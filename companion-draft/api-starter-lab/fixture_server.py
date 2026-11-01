"""Fixed response server on loopback only; deliberately NOT a Claude emulator."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

FIXTURES = json.loads(Path(__file__).with_name('fixtures.json').read_text())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if self.path != '/draft' or not 0 < size <= 8192:
                raise ValueError('invalid path or size')
            request = json.loads(self.rfile.read(size))
            case = FIXTURES[request['case']]
            if request['note'] != case['note']:
                raise ValueError('note differs from the fixed case')
        except (ValueError, KeyError, TypeError):
            self.send_error(400, 'Unknown or mismatched teaching case')
            return
        body = case['body']
        raw = body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(case.get('http_status', 200))
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def make_server(port=0):
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    with make_server(args.port) as server:
        print(f'Local fixed fixtures: http://127.0.0.1:{server.server_port}/draft', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
