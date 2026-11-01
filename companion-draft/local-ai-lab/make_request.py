"""Prepare one fictional request file; no network and no model download."""
import argparse
import json
from pathlib import Path


def build(case_id, model):
    if not model or model != model.strip() or any(c.isspace() for c in model):
        raise ValueError('record the exact installed local model identifier')
    if 'cloud' in model.lower() or model == 'YOUR_RECORDED_LOCAL_MODEL':
        raise ValueError('select an actual downloaded local model, not a cloud model or placeholder')
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    case = next((c for c in cases if c['id'] == case_id), None)
    if case is None:
        raise ValueError('unknown case')
    return {'model': model, 'prompt': case['task']+'\nSOURCE:\n'+case['source'],
            'stream': False, 'options': {'temperature': 0, 'num_ctx': 4096, 'num_predict': 256}}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case', required=True);p.add_argument('--model', required=True);p.add_argument('--out', required=True)
    a=p.parse_args();request=build(a.case,a.model)
    with Path(a.out).open('x') as f:json.dump(request,f,indent=2);f.write('\n')
    print('Prepared request only. Model presence, locality and runtime configuration must still be checked.')
