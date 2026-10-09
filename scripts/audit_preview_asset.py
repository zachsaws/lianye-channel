"""Check identity/category traceability, not category fit or cooperation truth."""
import json
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
class Cards(HTMLParser):
 def __init__(self):super().__init__();self.items=[];self.active=None;self.name=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='li' and 'channel-tile' in a.get('class',''):self.active={'id':a.get('data-id'),'directions':a.get('data-directions','').split(),'name':''}
  if t=='span' and self.active and a.get('class')=='channel-name':self.name=True
 def handle_data(self,d):
  if self.active and self.name:self.active['name']+=d
 def handle_endtag(self,t):
  if t=='span':self.name=False
  if t=='li' and self.active:self.items.append(self.active);self.active=None
# Explicit shortened display alias; never fuzzy-match names.
aliases={'雷音音频（深圳）有限公司':['雷音音频']}
p=Cards();p.feed((root/'site-preview/index.html').read_text());asset=json.loads((root/'research/current/channel-asset.json').read_text())['profiles'];byid={r['id']:r for r in asset}
assert len({c['id'] for c in p.items})==len(p.items)
for c in p.items:
 assert c['id'] in byid,c
 a=byid[c['id']];assert c['name'] in [a['displayName']]+aliases.get(a['displayName'],[]),c
 assert set(c['directions'])==set(a['directions']),c
 assert a['sourceLinks'] and not a['dispatchable'] and a['companyRelationship']=='not_established'
result={'scope':'preview_asset_identity_and_editorial_direction_consistency_only','cards':len(p.items),'assetProfiles':len(asset),'passed':True,'limits':['不证明分类适配','不证明来源事实','不证明合作或采购意愿']}
(root/'site-preview/review/asset-consistency.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
