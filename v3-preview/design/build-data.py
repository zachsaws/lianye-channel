import json,re,hashlib
from pathlib import Path
root=Path('.');p=root/'v3-preview';legacy=json.loads((root/'v22-preview/data/channels.json').read_text())['rows'];research=json.loads((root/'research/channels/researched-entities-v36.json').read_text())['records'];profiles=json.loads((root/'research/current/channel-asset.json').read_text())['profiles'];pm={x['displayName']:x for x in profiles};pi={x['id']:x for x in profiles};records=[];seen={};decisions=[]
def norm(n):return re.sub(r'[^a-z0-9\u4e00-\u9fff]','',n.lower()).replace('总统眼镜','').replace('博士眼镜','博士')
def subcat(name,role,path):
 text=name+' '+role
 if path=='content':
  if re.search('直播|交个朋友|东方甄选|遥望|东方购物',text):return '直播与内容经营'
  if re.search('影像|新片场|优设',text):return '设计与影像创作'
  return '科技与数码内容'
 if path=='community':return '会员与兴趣社群'
 if re.search('智玩店|INNO100|Z.?Pilot|AI机器时代|陶朱|Robot Mall|模速|龙岗.*6S|光谷.*7S|原力城市',text,re.I):return 'AI与创新产品体验'
 if re.search('机器人器材|教育|教学|幼教|教具|科创|创客教室|师训',text):return '教育与机构服务'
 if re.search('玩具|母婴|亲子|潮玩|孕婴|收藏|IP经营|IP消费|IP商品|IP衍生|TOY|孩子王|婴童',text,re.I):return '亲子与潮玩经营'
 if re.search('运动|户外|骑行|体育|赛事',text):return '运动与户外经营'
 if re.search('影音|家居|智能家|全屋智能|DK-AI',text):return '家居与影音空间'
 if re.search('眼镜|验配|LOHO',text):return '专业体验与验配'
 if re.search('软件|应用|云市场|云商店|飞书',text):return '软件与应用生态'
 if re.search('企业|政企|福利|礼赠|礼品|办公|集采|采购|供应链|分销|ICT|代理',text):
  if re.search('幼教|教育|科创|教具|机器人教育',text):return '教育与机构服务'
  if re.search('音乐|乐器|音响|音频',text):return '音乐与专业创作'
  if re.search('宠物',text):return '宠物与垂直经营'
  return '企业采购与专业分销'
 if re.search('影像|数码|相机|BITSHOP|中免|通讯|美承|京东|苏宁|顺电|九机',text):return '数码与影像零售'
 if re.search('眼镜|验配|光明|LOHO|听力',text):return '专业体验与验配'
 if re.search('母婴|亲子|玩具|潮玩|收藏|IP|宝宝|孕婴|TOY|孩子王|三月兽',text):return '亲子与潮玩零售'
 if re.search('影音|家居|家电|智能家|DK-AI',text):return '家居与影音空间'
 if re.search('运动|体育|户外|骑行|Garmin',text):return '运动与户外经营'
 if re.search('乐器|音乐|音频',text):return '音乐与专业创作'
 if re.search('书店|书局|书厦|书大厦|文创|杂物|生活方式',text):return '文化与生活方式'
 if re.search('教育|幼教|机器人教育',text):return '教育与机构服务'
 if re.search('宠物|易宠|波奇|派多格|宠老板',text):return '宠物与垂直经营'
 return 'AI与创新产品体验'
def pathfor(name,role,old=None):
 if old=='retail':return 'retail'
 if old in ['creator','content']:return 'content'
 if old=='community':return 'community'
 if re.search('直播|内容电商|内容零售|垂直内容',role):return 'content'
 if re.search('企业|政企|分销|供应链|机构|教学|教育经销|软件|应用|实训|器材采购|福利|集采|礼品|礼赠|ICT',role):return 'business'
 return 'retail'
def region(n):
 m=re.search('(北京|上海|深圳|广州|杭州|成都|重庆|武汉|南京|西安|天津|宁波|东莞|长沙|合肥|福州|银川|南宁|乌鲁木齐|新疆|河南|山东|浙江|江苏|广东|四川|辽宁|福建|宁夏|内蒙古)',n)
 return m.group(1) if m else '以来源为准'
def add(r):
 key=norm(r['name'])
 existing=seen.get(key) or next((z for z in records if z['id']==r['id']),None)
 if existing:
  if r['name']!=existing['name']:existing.setdefault('aliases',[]).append(r['name'])
  existing['sources']=list(dict.fromkeys(existing['sources']+r['sources']))
  return False
 seen[key]=r;records.append(r);return True
for r in legacy:
 prof=pi.get(r['id'],pm.get(r['name'],{}));e=prof.get('importedEvidence',[]);fact=(e[0].get('facts') if e else '') or r.get('tag','');role=r.get('kind','')+' '+r['tag'];path=pathfor(r['name'],role,r['path']);sub=subcat(r['name'],role,path)
 if path=='business' and sub not in ['软件与应用生态','教育与机构服务','音乐与专业创作','宠物与垂直经营','亲子与潮玩经营','运动与户外经营','家居与影音空间','AI与创新产品体验','专业体验与验配']:sub='企业采购与专业分销'
 add(dict(id=r['id'],name=r['name'],parent=r.get('parent',''),path=path,subcategory=sub,tag=r['tag'],directions=r.get('directions',[]),sources=r['sources'],facts=fact[:300],region=region(r['name']+' '+r['tag']),observed=r.get('observed','2026-10-08'),provenance='既有研究资料，未逐项实时复核',limits='公开经营资料不证明联野已合作、新品准入、可调动的受众或成交效果。',relationship='未建立合作'))
for i,r in enumerate(research):
 name=r['name'];ev=r.get('evidence',[]);role=' / '.join(dict.fromkeys(x.get('role','') for x in ev));src=list(dict.fromkeys(x.get('source','') for x in ev if x.get('source','').startswith('http')))
 if norm(name) in seen or any(len(norm(z['name']))>=3 and (norm(z['name']) in norm(name) or norm(name) in norm(z['name'])) for z in records):decisions.append({'name':name,'decision':'merged_existing'});continue
 if not src or not role or re.search('待核|待补',role) or i in range(153,161):decisions.append({'name':name,'decision':'not_promoted_scope_or_evidence'});continue
 path=pathfor(name,role);sub=subcat(name,role,path)
 if path=='business' and sub not in ['软件与应用生态','教育与机构服务','音乐与专业创作','宠物与垂直经营','亲子与潮玩经营','运动与户外经营','家居与影音空间','AI与创新产品体验','专业体验与验配']:sub='企业采购与专业分销'
 add(dict(id=hashlib.sha256(name.encode()).hexdigest()[:12],name=name,parent='',path=path,subcategory=sub,tag=role[:75],directions=r.get('directions',[]),sources=src,facts=ev[0].get('facts','')[:300],region=region(name),observed=ev[0].get('observed','2026-10-08'),provenance='既有研究拓展，分类仍需按项目核对',limits=ev[0].get('limits','不证明当前合作准入或销售能力。')[:250],relationship='未建立合作'));decisions.append({'name':name,'decision':'included_reference'})
checks=json.loads((p/'data/source-checks.json').read_text())
for r in checks:
 if re.search('停止|关闭|维护中',r.get('title','')):r['qualified']=False;r['reason']='官方显示服务已停止或不可用'
 if not r['qualified']:decisions.append({'name':r['name'],'decision':'new_source_not_qualified','reason':r.get('reason',r.get('error','内容未确认'))});continue
 add(dict(id=hashlib.sha256(r['name'].encode()).hexdigest()[:12],name=r['name'],parent='',path=r['path'],subcategory=r['subcategory'],tag=r['subcategory'],directions=['creative','office'] if r['path']=='community' else ['creative','wearable','office'],sources=[r['url']],facts='本次读取官方页面，识别为'+r['subcategory']+'的公开内容或交流入口；未核实商务合作条件。',region='线上 / 区域以来源为准',observed='2026-10-19',provenance='本次官方页面核查；只确认公开入口，不确认销售能力',limits='机构或平台存在不等于成员可触达、可发布推广、可带来销量；需遵守其规则并获得具体经营者授权。',relationship='未建立合作'))
(p/'data/source-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));payload={'date':'2026-10-19','scope':'公开市场通路研究参考，不是客户、签约伙伴或已开放网络','rows':records};(p/'data/channels.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2));(p/'data/channels.js').write_text('window.LIANYE_CHANNELS='+json.dumps(payload,ensure_ascii=False)+';');(p/'data/migration.json').write_text(json.dumps({'legacyIdsPreserved':all(any(z['id']==r['id'] for z in records) for r in legacy),'decisions':decisions},ensure_ascii=False,indent=2));print('records',len(records));print({k:sum(r['path']==k for r in records)for k in ['retail','content','community','business']});print('subcategories',len(set(r['subcategory'] for r in records)))
