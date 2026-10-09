"""Keep research candidates separate from paused and unsupported routes.
This adapter does not judge procurement fit or modify raw model output.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]; p=root/'research/prototype'
raw=json.loads((p/'independent-ai-output-v3.json').read_text())
paused={'pause_product_preparation','pause_deployment_prepare_compatibility','prepare_classroom_package_then_recheck','investigate_software_route_pause_channel_sale'}
verify={'first_verify','secondary_fit_check','conditional_low_priority'}
unsupported={'do_not_prioritize'}
rows=[]
for case in raw['cases']:
 buckets={'verify_fit':[],'conditions_first':[],'not_supported_by_snapshot':[],'manual_review':[]}
 for route in case['routes']:
  status=route['status']
  if status in unsupported: bucket='not_supported_by_snapshot'
  elif case['decision'] in paused: bucket='conditions_first'
  elif status in verify: bucket='verify_fit'
  else: bucket='manual_review'
  buckets[bucket].append({'name':route['displayName'],'rawStatus':status,'reason':route['reason'],'evidence':route['evidence'],'unknown':route['unknown'],'nextQuestion':route.get('nextQuestion'),'eligibleForAutomaticOutreach':False})
 rows.append({'caseId':case['caseId'],'rawDecision':case['decision'],'buckets':buckets,'unknown':case['unknown']})
result={'scope':'research_review_only_not_sales_recommendations','mappingMethod':'explicit_case_and_route_status_mapping','inputSHA256':raw['inputSHA256'],'cases':rows,'limits':'暂停是准备条件不足，不等于渠道拒绝；不支持是本快照证据不足，不等于永久不适配；所有外联须人核实与授权。'}
# Check high-risk counterexamples rather than only JSON shape.
byid={c['caseId']:c for c in rows}
assert not byid['wearable-clinical-only']['buckets']['verify_fit']
for key in ['companion-no-demo','office-service-withdrawn','home-installed-controller','learning-classroom-tool','creative-transcription-subscription']:
 assert not byid[key]['buckets']['verify_fit'],key
assert sum(len(v) for c in rows for v in c['buckets'].values())==sum(len(c['routes']) for c in raw['cases'])
assert all(not r['eligibleForAutomaticOutreach'] for c in rows for rs in c['buckets'].values() for r in rs)
(p/'normalized-research-decisions-v3.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('All original routes retained; paused and unsupported cases cannot appear as active fit candidates.')
