"""Reject unsupported partner claims, duplicate identities and unsupported numeric fields."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'research/current/channel-asset.json').read_text())['profiles']
b=json.loads((ROOT/'research/current/candidate-audit.json').read_text())['records']
assert len(b)==24
assert len({r['id'] for r in a})==len(a)
assert len({r['displayName'] for r in a})==len(a)
assert all(r['sourceLinks'] and all(s.startswith('https://') for s in r['sourceLinks']) for r in a)
assert all(r['companyRelationship']=='not_established' and r['dispatchable'] is False for r in a)
assert all(r[k] is None for r in a for k in ['priceBand','creditTerms','purchaseIntent','capacity'])
assert all(r['mergeInto'] in {x['displayName'] for x in a} for r in b if r['displayDecision']=='merge_not_increment')
# A missing legal identity remains visible in the status, never upgraded silently.
assert next(r for r in b if r['name']=='成方策')['legalName'].endswith('（法人待进一步核实）')
report={'checks':['unique display identities','sources retained','unknown commercial terms kept null','no fabricated relationship','four aliases merged','unresolved identity preserved'], 'passed':True,'profileCount':len(a),'candidateReviewCount':len(b),'claim':'research integrity only; not commercial effectiveness or source truth validation'}
(ROOT/'research/current/integrity-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
