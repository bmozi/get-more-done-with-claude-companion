"""Local deterministic Chapter 47 lab. No scheduler, model, network, or messaging."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3


def connect(path):
    db = sqlite3.connect(path, timeout=10, isolation_level=None)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS reports(period TEXT PRIMARY KEY, body TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, period TEXT NOT NULL,
        run_date TEXT NOT NULL, status TEXT NOT NULL, detail TEXT NOT NULL, source_hash TEXT);
    ''')
    return db


def prepare(raw, period, run_date):
    data = json.loads(raw)
    if not isinstance(data, dict) or not isinstance(data.get('tasks'), list):
        raise ValueError('source must be an object with a tasks list')
    confirmed = date.fromisoformat(data['confirmed'])
    if not 0 <= (run_date - confirmed).days <= 7:
        raise ValueError('source must be confirmed within seven days of execution')
    due, unknown, seen = [], [], set()
    for row in data['tasks']:
        if not isinstance(row, dict):
            raise ValueError('each task must be an object')
        identifier = row['id']
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError('missing or duplicate task ID')
        seen.add(identifier)
        if row['status'] not in ('Open', 'Done'):
            raise ValueError('unknown task status')
        deadline = date.fromisoformat(row['due']) if row['due'] is not None else None
        if row['status'] == 'Done':
            continue
        if deadline is None:
            unknown.append(identifier)
        elif deadline <= period:
            due.append(identifier)
    return {'period': period.isoformat(), 'due': sorted(due), 'unknown': sorted(unknown),
            'due_count': len(due), 'unknown_count': len(unknown),
            'confirmed': data['confirmed']}


def run(database, source, period, run_date, fault=None):
    period, run_date = date.fromisoformat(period), date.fromisoformat(run_date)
    if run_date < period:
        raise ValueError('run date cannot precede reporting period')
    db = connect(database)
    try:
        # One writer checks completion and publishes inside the same transaction.
        db.execute('BEGIN IMMEDIATE')
        key = period.isoformat()
        if db.execute('SELECT 1 FROM reports WHERE period=?', (key,)).fetchone():
            db.execute('INSERT INTO attempts(period,run_date,status,detail) VALUES(?,?,?,?)',
                       (key, run_date.isoformat(), 'skipped', 'period already completed'))
            db.commit()
            return {'status': 'skipped', 'period': key}
        digest = None
        try:
            raw = Path(source).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            body = prepare(raw, period, run_date)
            status = 'interrupted' if fault == 'after-prepare' else 'completed'
            detail = json.dumps(body, sort_keys=True)
        except (OSError, ValueError, KeyError, TypeError) as error:
            status, detail = 'failed', f'{type(error).__name__}: {error}'
        if status == 'completed':
            db.execute('INSERT INTO reports VALUES(?,?)', (key, detail))
        db.execute('INSERT INTO attempts(period,run_date,status,detail,source_hash) VALUES(?,?,?,?,?)',
                   (key, run_date.isoformat(), status, detail, digest))
        db.commit()
        # after-commit imitates a lost acknowledgement, not a failed database write.
        if fault == 'after-commit' and status == 'completed':
            return {'status': 'acknowledgement-lost', 'period': key}
        return {'status': status, 'period': key, 'detail': detail}
    finally:
        db.close()


def inspect(database):
    # Read-only inspection must not create a new ledger after a path typo.
    uri = Path(database).resolve().as_uri() + '?mode=ro'
    db = sqlite3.connect(uri, uri=True)
    try:
        return {'reports': [json.loads(r[0]) for r in db.execute('SELECT body FROM reports ORDER BY period')],
                'attempts': [dict(zip(('id','period','run_date','status','detail','source_hash'), r))
                             for r in db.execute('SELECT * FROM attempts ORDER BY id')]}
    finally:
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True)
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--source')
    parser.add_argument('--period')
    parser.add_argument('--run-date')
    parser.add_argument('--fault', choices=('after-prepare', 'after-commit'))
    args = parser.parse_args()
    if args.inspect:
        result = inspect(args.db)
    else:
        if not all((args.source, args.period, args.run_date)):
            parser.error('--source, --period, --run-date required for a run')
        result = run(args.db, args.source, args.period, args.run_date, args.fault)
    print(json.dumps(result, indent=2))
    raise SystemExit(2 if result.get('status') in ('failed','interrupted','acknowledgement-lost') else 0)
