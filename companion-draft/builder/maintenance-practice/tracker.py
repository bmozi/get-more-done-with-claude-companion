"""Fictional read-only teaching baseline. Standard library; no API calls."""
import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import sys


def parse_date(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'invalid ISO date: {value!r}; expected YYYY-MM-DD')
    return date.fromisoformat(value)


def report(path, as_of):
    groups = {name: [] for name in ('due', 'future', 'done', 'unknown')}
    seen = set()
    with Path(path).open(newline='', encoding='utf-8') as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ['id', 'item', 'due_date', 'status']:
            raise ValueError('expected columns: id,item,due_date,status')
        for line, row in enumerate(reader, 2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'line {line}: wrong number of fields')
            row = {k: v.strip() for k, v in row.items()}
            if not row['id'] or not row['item']:
                raise ValueError(f'line {line}: id and item must be present')
            if row['id'] in seen:
                raise ValueError(f'line {line}: duplicate id {row["id"]}')
            seen.add(row['id'])
            if row['status'] not in ('open', 'done'):
                raise ValueError(f'line {line}: unsupported status {row["status"]!r}')
            try:
                due = parse_date(row['due_date']) if row['due_date'] else None
            except ValueError as exc:
                raise ValueError(f'line {line}: {exc}') from exc
            group = ('done' if row['status'] == 'done' else 'unknown' if due is None
                     else 'due' if due <= as_of else 'future')
            groups[group].append(row)
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--as-of', required=True)
    args = parser.parse_args()
    try:
        result = report(args.input, parse_date(args.as_of))
    except (OSError, ValueError, csv.Error) as exc:
        print(f'Cannot produce report: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
