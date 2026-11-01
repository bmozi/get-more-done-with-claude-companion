"""Recompute fixture arithmetic and inspect source references; no model calls."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
packet=json.loads((root/'packet.json').read_text());key=json.loads((root/'answer-key.json').read_text())
s={x['id']:x for x in packet['sources']}
assert len(s)==len(packet['sources'])
occupancy=s['S2']['confirmed_guests']+s['S2']['staff']
cost=sum(s['S3'][x] for x in ['rental','cleaning','projector'])
assert occupancy==key['base']['occupancy']==35
assert s['S1']['capacity_people']-occupancy==key['base']['spare_capacity']==5
assert cost==key['base']['total_cost']==300
assert s['S3']['budget']-cost==key['base']['budget_remaining']==50
assert 38+s['S2']['staff']==key['variation']['occupancy']==41
assert s['S1']['capacity_people']-41==key['variation']['spare_capacity']==-1
assert max(0,key['variation']['occupancy']-s['S1']['capacity_people'])==key['variation']['required_occupancy_reduction']==1
assert {c['id'] for c in packet['draft_claims']}=={c['id'] for c in key['claims']}
for c in key['claims']:
 assert set(c['sources'])<=set(s)
 assert c['status'] in {'supported','contradicted','not established'}
print(json.dumps({'status':'passed','claims':len(key['claims']),'occupancy':occupancy,'spare_capacity':5,'cost':cost,'budget_remaining':50,'variation_occupancy':41,'scope':'fixture arithmetic and reference integrity; semantic judgments require source review'}))
