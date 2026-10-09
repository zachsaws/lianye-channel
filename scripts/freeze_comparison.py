"""Freeze identical evidence for fixed-rule and model comparison; keep older packets."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/prototype'
packet=json.loads((P/'independent-input-v2.json').read_text())
asset=json.loads((ROOT/'research/current/channel-asset.json').read_text())
byname={r['displayName']:r for r in asset['profiles']}
reviews=json.loads((ROOT/'research/current/reviewed-profile-details.json').read_text())['records']
channels=[]
for review in reviews:
 r=byname[review['displayName']]
 channels.append({'displayName':r['displayName'],'directions':r['directions'],'fields':review['fields'],'fieldEvidence':r['fieldEvidence'],'unknown':review['unknown'],'source':review['source'],'additionalSources':review.get('additionalSources',[]),'basis':review['basis'],'observed':review['observed'],'inferenceBoundary':review['inferenceBoundary']})
packet['version']=3
packet['channelEvidence']={'records':channels}
packet['comparisonBoundary']='同一快照；分类为编辑方向，经营字段为公开证据；无合作过程或销售结果。规则不阅读自然语言产品描述，仅处理已结构化字段。'
raw=json.dumps(packet,ensure_ascii=False,indent=2)
(P/'independent-input-v3.json').write_text(raw)
manifest={'version':3,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'caseCount':len(packet['productCases']),'channelEvidenceCount':len(channels),'modelExecutionStatus':'not_run','authorizationStatus':'isolated_agent_request_pending','previousPacket':'independent-input-v2.json preserved','comparisonStatus':'not_proven'}
(P/'independent-run-manifest-v3.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Frozen shared packet with',len(channels),'reviewed channel profiles.')
