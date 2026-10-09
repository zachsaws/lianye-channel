"""Read the public sales directory endpoint used by Garmin's official page; no private access."""
import urllib.request,urllib.parse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
url='https://www.garmin.com.cn/buy/get_json_data-server/cn/retailer/'
rows=[]
for start in range(0,100,25):
 params={'draw':1,'start':start,'length':25,'city':'','cat':'sports-recreation','type':'','search[value]':''}
 req=urllib.request.Request(url,data=urllib.parse.urlencode(params).encode(),headers={'Referer':'https://www.garmin.com.cn/buy/retailer/'})
 page=json.load(urllib.request.urlopen(req,timeout=20))
 rows+=page.get('data',[])
 if len(rows)>=int(page.get('recordsFiltered',0)):break
seen={};records=[]
for r in rows:
 if r['id'] in seen:continue
 seen[r['id']]=True
 name=r['title'].strip();kind='legal_name_directory_lead' if '有限公司' in name else 'store_or_trade_name_identity_unresolved'
 if '三夫户外' in name or '顺电' in name:kind='chain_store_not_independent_buyer'
 if '专柜' in name:kind='brand_counter_not_independent_buyer'
 records.append({'directoryId':r['id'],'name':name,'regionLabels':[x['eng'] for x in r.get('city',[])],'productSeries':[x['eng'] for x in r.get('series',[]) if x['eng']],'identityStatus':kind,'source':'https://www.garmin.com.cn/buy/retailer/','observed':'2026-10-09','unknown':['当前是否营业','独立采购权','跨品牌经营范围','新品引入政策'],'dispatchable':False})
output={'sourceEndpoint':url,'queryCategory':'sports-recreation','records':records,'boundary':'品牌销售据点，不是独立采购主体清单；区域标签来自目录，不证明区域代理权。没有保留个人电话、邮箱或精确地址。'}
(ROOT/'research/current/garmin-directory-review.json').write_text(json.dumps(output,ensure_ascii=False,indent=2))
print('Read',len(records),'unique directory rows; no partner or independent-buyer count inferred.')
