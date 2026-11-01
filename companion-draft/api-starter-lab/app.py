"""Local HTTP teaching application. No model, provider, account, or saving path."""
import argparse
from datetime import date
from http.client import HTTPException
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, ProxyHandler

LIMIT = 8192


def validate_input(note):
    if not isinstance(note, str) or not note.strip() or len(note) > 1000:
        raise ValueError('note must contain 1 to 1000 characters')


def validate_record(record, note):
    if not isinstance(record, dict) or set(record) != {'item', 'due_date', 'questions'}:
        raise ValueError('expected only item, due_date, questions')
    item, due, questions = record['item'], record['due_date'], record['questions']
    if not isinstance(item, str) or not item.strip() or item not in note:
        raise ValueError('item must be a nonempty literal span of the note')
    if not isinstance(questions, list) or any(not isinstance(q, str) or not q.strip() for q in questions):
        raise ValueError('questions must be a list of nonempty strings')
    if due is None:
        if not questions:
            raise ValueError('an unresolved date needs a question')
    else:
        if not isinstance(due, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', due):
            raise ValueError('date must use YYYY-MM-DD or null')
        date.fromisoformat(due)
        if due not in note:
            raise ValueError('this teaching contract requires a literal ISO date in the source')
    return record


def request_draft(endpoint, note, case, timeout=2):
    validate_input(note)  # Failure here must make zero requests.
    parsed = urlparse(endpoint)
    if (parsed.scheme != 'http' or parsed.hostname != '127.0.0.1' or
            parsed.username or parsed.password or parsed.path != '/draft' or
            parsed.query or parsed.fragment):
        raise ValueError('use only the local teaching endpoint http://127.0.0.1:PORT/draft')
    request = Request(endpoint, json.dumps({'note': note, 'case': case}).encode(),
                      {'Content-Type': 'application/json'}, method='POST')
    # No system proxy or redirect to a remote host is needed in this exercise.
    import urllib.request
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = build_opener(ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(LIMIT + 1)
    except HTTPError as exc:
        raise ValueError(f'HTTP {exc.code}; no draft accepted and no automatic retry') from exc
    except (URLError, TimeoutError, OSError, HTTPException) as exc:
        raise ValueError('transport failed or timed out; no draft accepted') from exc
    if len(raw) > LIMIT:
        raise ValueError('response exceeded the teaching size limit')
    def unique_fields(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON field')
            result[key] = value
        return result
    try:
        envelope = json.loads(raw, object_pairs_hook=unique_fields)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError('response is not valid unambiguous JSON') from exc
    if not isinstance(envelope, dict) or envelope.get('status') != 'complete':
        raise ValueError('response did not report complete; no draft accepted')
    record = validate_record(envelope.get('record'), note)
    return {'state': 'draft_for_review', 'record': record,
            'evidence_kind': 'local_fixed_fixture_not_model_output'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--endpoint', required=True)
    parser.add_argument('--case', default='complete')
    parser.add_argument('--note', required=True)
    args = parser.parse_args()
    try:
        result = request_draft(args.endpoint, args.note, args.case)
    except ValueError as exc:
        print(json.dumps({'state': 'rejected', 'reason': str(exc)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
