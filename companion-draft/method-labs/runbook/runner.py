"""Read-only, deterministic reference for the fictional Chapter 41 runbook."""
import argparse
import json
from pathlib import Path

FIXTURES = Path(__file__).with_name('fixtures.json')


def summarize(case):
    rows = case['rows']
    result = {
        'source_id': case['source_id'],
        'source_rows': len(rows),
        'distinct_registration_ids': len({r['id'] for r in rows}),
        'people': None,
        'known_subtotal': None,
        'excluded_source_rows': [],
        'issues': [],
        'output_state': 'draft',
        'review_state': 'pending_coordinator_review',
    }
    for row in rows:
        if not isinstance(row['id'], str) or not row['id'].strip():
            raise ValueError('Each source row requires an identifier')
        count = row['people']
        if count is not None and (type(count) is not int or count < 0):
            raise ValueError('People must be a nonnegative whole number or null')
        if row['meaning'] not in ('current', 'accidental_copy', 'amendment'):
            raise ValueError('Unknown record meaning requires clarification')

    # Amendment semantics must be resolved before any deduplication or total.
    if any(r['meaning'] == 'amendment' for r in rows):
        result['issues'] = ['Clarify whether amendments replace or supplement earlier records.']
        result['count_state'] = 'unresolved_record_meaning'
        return result

    kept = []
    for number, row in enumerate(rows, 1):
        if row['meaning'] == 'accidental_copy':
            if not any(r['id'] == row['id'] and r['people'] == row['people'] for r in kept):
                raise ValueError('Declared accidental copy has no matching retained record')
            result['excluded_source_rows'].append(number)
        else:
            if any(r['id'] == row['id'] for r in kept):
                raise ValueError('Repeated identifier without an accidental-copy rule')
            kept.append(row)
    missing = [r['id'] for r in kept if r['people'] is None]
    subtotal = sum(r['people'] for r in kept if r['people'] is not None)
    if missing:
        result['known_subtotal'] = subtotal
        result['issues'] = ['Clarify missing people count: ' + ', '.join(missing) + '.']
        result['count_state'] = 'incomplete'
    else:
        result['people'] = subtotal
        result['count_state'] = 'complete'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, choices=('normal', 'missing', 'amendment'))
    args = parser.parse_args()
    cases = json.loads(FIXTURES.read_text(encoding='utf-8'))
    print(json.dumps(summarize(cases[args.case]), indent=2))


if __name__ == '__main__':
    main()
