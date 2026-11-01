"""Check supplied fictional arithmetic. Does not call Claude or evaluate a learner."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]

def results():
    with (ROOT / 'career/tickets.csv').open() as source:
        rows = list(csv.DictReader(source))
    latest = {}
    for row in rows:
        current = latest.get(row['ticket_id'])
        if current is None or row['updated'] > current['updated']:
            latest[row['ticket_id']] = row
    def counts(records):
        return {state: sum(row['state'] == state for row in records.values())
                for state in ('Open', 'Closed', 'Waiting')}
    baseline = counts(latest)
    overdue = sum(r['state'] == 'Open' and r['overdue'] == 'yes' for r in latest.values())
    changed = dict(latest)
    changed['T03'] = dict(ticket_id='T03', updated='2026-10-28', state='Waiting', overdue='no')
    job = json.loads((ROOT / 'business/job.json').read_text())
    remainder = job['price'] - job['direct_cash_cost']
    before_receipt = job['deposit_received'] - job['direct_cash_cost']
    calculated = {
        'source_rows': len(rows), 'distinct_tickets': len(latest),
        'baseline_states': baseline, 'baseline_open_overdue': overdue,
        'changed_states': counts(changed),
        'direct_cost_remainder': remainder,
        'four_hour_remainder_before_excluded_costs': remainder - job['planned_hours'] * job['time_value_per_hour'],
        'six_hour_remainder_before_excluded_costs': remainder - job['overrun_hours'] * job['time_value_per_hour'],
        'cash_before_final_receipt': before_receipt,
        'cash_after_final_receipt': before_receipt + job['later_final_payment_received'],
        'gap_before_new_job': max(0, job['next_job_direct_spend_before_new_receipt'] - before_receipt),
    }
    expected = {'source_rows': 6, 'distinct_tickets': 5,
                'baseline_states': {'Open': 2, 'Closed': 2, 'Waiting': 1},
                'baseline_open_overdue': 1,
                'changed_states': {'Open': 2, 'Closed': 1, 'Waiting': 2},
                'direct_cost_remainder': 160,
                'four_hour_remainder_before_excluded_costs': 40,
                'six_hour_remainder_before_excluded_costs': -20,
                'cash_before_final_receipt': 70, 'cash_after_final_receipt': 160,
                'gap_before_new_job': 10}
    if calculated != expected:
        raise ValueError({'calculated': calculated, 'expected': expected})
    return {'status': 'passed', 'calculated': calculated,
            'limits': 'Local source arithmetic only; no Claude session or human trial.'}

if __name__ == '__main__':
    print(json.dumps(results(), indent=2))
