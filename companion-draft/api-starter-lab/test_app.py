import contextlib
import io
import json
import threading
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import app
from fixture_server import FIXTURES, make_server


class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server()
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.endpoint = f'http://127.0.0.1:{cls.server.server_port}/draft'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def run_case(self, name):
        return app.request_draft(self.endpoint, FIXTURES[name]['note'], name)

    def test_complete_http_roundtrip_is_draft_only(self):
        result = self.run_case('complete')
        self.assertEqual(result['state'], 'draft_for_review')
        self.assertEqual(result['record']['due_date'], '2026-10-20')

    def test_missing_year_remains_unknown(self):
        self.assertIsNone(self.run_case('missing-year')['record']['due_date'])

    def test_failure_boundaries(self):
        for case in ['impossible-date', 'extra-field', 'invented-date', 'wrong-item',
                     'incomplete', 'malformed', 'http-failure']:
            with self.subTest(case=case), self.assertRaises(ValueError):
                self.run_case(case)

    def test_empty_input_never_constructs_transport(self):
        with patch('app.build_opener') as opener, self.assertRaises(ValueError):
            self.run_case('empty')
        opener.assert_not_called()

    def test_remote_endpoint_rejected_before_transport(self):
        with patch('app.build_opener') as opener, self.assertRaises(ValueError):
            app.request_draft('https://example.com/draft', 'note', 'complete')
        opener.assert_not_called()

    def test_timeout_stops_without_retry(self):
        with patch('app.build_opener') as factory:
            factory.return_value.open.side_effect = TimeoutError('designed test')
            with self.assertRaisesRegex(ValueError, 'timed out'):
                self.run_case('complete')
            self.assertEqual(factory.return_value.open.call_count, 1)

    def run_raw_response(self, body, valid_http=True):
        class RawHandler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                if valid_http:
                    self.send_response(200)
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                self.wfile.write(body)
        server = ThreadingHTTPServer(('127.0.0.1', 0), RawHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            return app.request_draft(f'http://127.0.0.1:{server.server_port}/draft',
                                     FIXTURES['complete']['note'], 'complete')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_malformed_http_is_a_controlled_failure(self):
        with self.assertRaisesRegex(ValueError, 'transport failed'):
            self.run_raw_response(b'NOTHTTP\r\n\r\n', valid_http=False)

    def test_duplicate_json_fields_rejected(self):
        for raw in [
            b'{"status":"incomplete","status":"complete","record":{"item":"filter","due_date":"2026-10-20","questions":[]}}',
            b'{"status":"complete","record":{"item":"wrong","item":"filter","due_date":"2026-10-20","questions":[]}}'
        ]:
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'unambiguous JSON'):
                self.run_raw_response(raw)

    def test_missing_question_rejected(self):
        with self.assertRaises(ValueError):
            app.validate_record({'item':'filter','due_date':None,'questions':[]}, 'filter')

    def test_wrong_question_type_rejected(self):
        with self.assertRaises(ValueError):
            app.validate_record({'item':'filter','due_date':None,'questions':'when?'}, 'filter')

    def test_negation_is_an_explicit_semantic_limit(self):
        # Literal checks cannot detect that the proposed action contradicts the note.
        result = app.validate_record({'item':'filter','due_date':'2026-10-20','questions':[]},
                                     'Do not replace the filter on 2026-10-20.')
        self.assertEqual(result['item'], 'filter')


if __name__ == '__main__':
    unittest.main()
