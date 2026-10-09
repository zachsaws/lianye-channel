"""Build auditable research profiles without expanding partner or authorization claims."""
import json,re,hashlib
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Cards(HTMLParser):
 def __init__(self):super().__init__();self.cards=[];self.card=None;self.field=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='li' and 'channel-tile' in a.get('class',''):
   self.card={'id':a.get('data-id'),'directions':a.get('data-directions','').split(),'search':a.get('data-search','')}
  if tag=='span' and self.card:
   self.field={'channel-name':'name','channel-tag':'tag'}.get(a.get('class'))
 def handle_data(self,data):
  if self.card and self.field:self.card[self.field]=self.card.get(self.field,'')+data
 def handle_endtag(self,tag):
  if tag=='span':self.field=None
  if tag=='li' and self.card:self.cards.append(self.card);self.card=None
parser=Cards();parser.feed((ROOT/'site/index.html').read_text())
source=json.loads((ROOT/'research/channels/source-map-current.json').read_text())
records=json.loads((ROOT/'research/channels/researched-entities-v36.json').read_text())['records']
byname={r['name']:r for r in records};sources={r['name']:r for r in source['rows']}
profiles=[]
def walk(value):
 if isinstance(value,dict):
  yield value
  for child in value.values():yield from walk(child)
 elif isinstance(value,list):
  for child in value:yield from walk(child)
supplement=[]
for path in (ROOT/'research/channels').glob('*oct08.json'):
 for obj in walk(json.loads(path.read_text())):
  if obj.get('name'):supplement.append((path.name,obj))
for card in parser.cards:
 mapping=sources[card['name']]
 matched=[byname[n] for n in mapping['recordNames'] if n in byname]
 evidence=[]
 for r in matched:
  for e in r.get('evidence',[]):
   if e.get('source') in mapping['sources']:evidence.append(e)
 # Import only exact recorded identities; a shared directory URL never proves a shared actor.
 for origin,obj in supplement:
  if obj['name'] in mapping['recordNames'] or obj['name']==card['name']:
   for e in obj.get('evidence',[]):
    if isinstance(e,dict) and e.get('source') in mapping['sources']:
     evidence.append({**e,'importFile':origin})
   if obj.get('source') in mapping['sources'] and (obj.get('facts') or obj.get('evidenceScope')):
    evidence.append({'source':obj['source'],'facts':obj.get('facts',obj.get('evidenceScope')),'limits':obj.get('limits',obj.get('evidenceScope')),'observed':obj.get('observed',obj.get('documentDate')),'state':'historical_supplement_import','importFile':origin})
 # Roles are editorial until reviewed against source evidence.
 tag=card['tag'];roles=[]
 for role,words in [('distribution',['分销','代理','经销','供应链','供货']),('retail',['零售','书店','体验','百货']),('institutional_purchase',['采购','集采','福利','礼赠','团购','园所','教育器材']),('integration',['集成','部署','方案','系统']),('content_commerce',['直播','电商','内容'])]:
  if any(w in tag for w in words):roles.append(role)
 profiles.append({'id':card['id'],'displayName':card['name'],'recordNames':mapping['recordNames'],'directions':card['directions'],'editorialTag':tag,'editorialRoles':roles,'roleStatus':'tag_based_hypothesis_not_source_verification','sourceLinks':mapping['sources'],'importedEvidence':evidence,'evidenceStatus':'historical_research_import_not_live_revalidation','researchGaps':[] if evidence else ['原始记录未在本轮导入的规范库找到；需要回查专题资料'],'buyerScenarios':[],'productScope':[],'regions':[],'entryPoints':[],'deliveryRequirements':[],'afterSalesRequirements':[],'priceBand':None,'creditTerms':None,'purchaseIntent':None,'capacity':None,'companyRelationship':'not_established','dispatchable':False,'displayStatus':'existing_public_market_route'})
# Keep reviewed candidates separate from current website and preserve unresolved legal names.
audit=json.loads((ROOT/'research/current/candidate-audit.json').read_text())
for r in audit['records']:
 if r['displayDecision']=='candidate_for_editorial_review':
  profiles.append({'id':'research-'+hashlib.sha256(r['name'].encode()).hexdigest()[:12],'displayName':r['name'],'recordNames':[r['legalName']],'directions':[{'陪伴与亲子':'companion','家庭与空间':'home','运动与穿戴':'wearable','创作与数码':'creative','学习与教育':'learning','办公与生产力':'office'}[r['direction']]],'editorialTag':r['role'],'editorialRoles':[],'roleStatus':'review_required','sourceLinks':r['reviewSources'],'reviewFinding':r['reviewFinding'],'identityStatus':r['identityStatus'],'evidenceStatus':'operator_scope_read_oct09','researchGaps':[r.get('reviewBoundary',r['limits'])],'buyerScenarios':[],'productScope':[],'regions':[],'entryPoints':[],'deliveryRequirements':[],'afterSalesRequirements':[],'priceBand':None,'creditTerms':None,'purchaseIntent':None,'capacity':None,'companyRelationship':'not_established','dispatchable':False,'displayStatus':'candidate_not_in_website'})
# Preserve independently reviewed details across rebuilds, including field-level provenance.
details_path=ROOT/'research/current/reviewed-profile-details.json'
if details_path.exists():
 for review in json.loads(details_path.read_text())['records']:
  matches=[p for p in profiles if p['displayName']==review['displayName']]
  if len(matches)!=1:raise ValueError('Reviewed identity must match exactly once: '+review['displayName'])
  profile=matches[0]
  for field,value in review['fields'].items():profile[field]=value
  profile.setdefault('reviewedDetails',[]).append(review)
  if review['source'] not in profile['sourceLinks']:profile['sourceLinks'].append(review['source'])
output=ROOT/'research/current/channel-asset.json'
output.write_text(json.dumps({'schemaVersion':1,'scope':'domestic','profiles':profiles},ensure_ascii=False,indent=2))
print(f'Built {len(parser.cards)} existing profiles and {len(profiles)-len(parser.cards)} research candidates; no website changes.')
