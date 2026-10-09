"""Evidence-conservative readiness baseline, not an AI evaluator or sales predictor."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
asset=json.loads((ROOT/'research/current/channel-asset.json').read_text())
cases=json.loads((ROOT/'research/prototype/cases.json').read_text())['cases']
results=[]
for case in cases:
 missing=[field for field in ('demoReady','serviceOwnerKnown','fulfillmentKnown') if case.get(field) is not True]
 routes=[]
 if not missing:
  for p in asset['profiles']:
   if not p.get('reviewedDetails'):continue
   scope=' '.join(p.get('productScope',[])+p.get('buyerScenarios',[])+p.get('deliveryRequirements',[]))
   cross_recall=case['delivery']=='software' and any(term in scope for term in ('软件','IT管理','设备管理'))
   if case['direction'] not in p['directions'] and not cross_recall:continue
   routes.append({'name':p['displayName'],'decision':'unresolved_business_model_fit' if case.get('channelFitConditions') else 'research_further_not_purchase_recommendation','basis':p['reviewedDetails'],'recallBasis':'explicit_scope_keyword' if cross_recall else 'editorial_direction','priorityEstablished':False,'fitConditions':case.get('channelFitConditions',{}), 'fitWarning':'方向标签不能证明采购场景与交付方式一致；应先核实经营适配' if case.get('channelFitConditions') else None,'questions':['采购决策主体是谁？','是否接受该类新品？','商业及服务条件是什么？']+(['谁负责部署、账号和持续支持？'] if case['delivery']=='software' else [])})
 results.append({'caseId':case['id'],'decision':'complete_product_information_first' if missing else 'verify_channel_conditions','missingProductConditions':missing,'routesForFurtherResearch':routes,'limits':'产品方向相同仅支持进一步核实；未验证采购意愿、匹配效果或销量。'})
(ROOT/'research/prototype/baseline-results.json').write_text(json.dumps({'method':'fixed_rules','aiRun':False,'results':results},ensure_ascii=False,indent=2))
print('Saved readiness baseline for',len(results),'hypothetical inputs; AI comparison remains pending.')
