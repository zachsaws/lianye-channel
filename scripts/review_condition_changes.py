"""Compare versioned hypothetical decisions, preserving uncertainty and exact inputs."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/prototype'
cases={x['id']:x for x in json.loads((P/'cases.json').read_text())['cases']}
results={x['caseId']:x for x in json.loads((P/'baseline-results.json').read_text())['results']}
changes=[]
for pair in json.loads((P/'change-pairs.json').read_text())['pairs']:
 before,after=cases[pair['before']],cases[pair['after']]
 a,b=results[pair['before']],results[pair['after']]
 fields={k:{'before':before.get(k),'after':after.get(k)} for k in before.keys()|after.keys() if k not in ('id','description') and before.get(k)!=after.get(k)}
 previous={r['name']:r for r in a['routesForFurtherResearch']}
 current={r['name']:r for r in b['routesForFurtherResearch']}
 effects=[]
 for name,route in previous.items():
  if name not in current:effects.append({'name':name,'effect':'paused_due_to_product_readiness','notEquivalentTo':'渠道拒绝或不适配'})
  elif route['decision']!=current[name]['decision']:effects.append({'name':name,'effect':'recheck_business_fit','notEquivalentTo':'确认不能合作'})
  else:effects.append({'name':name,'effect':'no_decision_change_observed'})
 passed=(bool(previous) and not current and b['decision']=='complete_product_information_first') if pair['expectedEffect']=='pause_preparation' else any(e['effect']=='recheck_business_fit' for e in effects)
 changes.append({**pair,'changedFields':fields,'beforeDecision':a['decision'],'afterDecision':b['decision'],'affectedRoutes':effects,'expectedEffectObserved':passed})
output={'method':'fixed_rule_version_comparison','aiRun':False,'caseInputSha256':hashlib.sha256((P/'cases.json').read_bytes()).hexdigest(),'resultInputSha256':hashlib.sha256((P/'baseline-results.json').read_bytes()).hexdigest(),'changes':changes,'limits':'仅证明这些假设输入下规则状态变化；不是AI效果或实际经营结果。'}
(P/'condition-change-results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
if not all(x['expectedEffectObserved'] for x in changes):raise SystemExit('Expected hypothetical change not observed')
print('Three hypothetical version changes reviewed; no channel refusal or AI effect inferred.')
