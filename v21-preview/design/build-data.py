import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
legacy=json.loads((root.parent/'research/current/channel-asset.json').read_text())['profiles']
rows=[];migration=[]
for p in legacy:
 roles=p.get('editorialRoles',[])
 path='retail' if 'retail' in roles else 'extended'
 kind='零售与体验' if path=='retail' else '专业通路'
 if path=='extended':
  if 'distribution' in roles:kind='专业分销'
  elif 'institutional_purchase' in roles:kind='企业与机构'
  elif 'integration' in roles:kind='集成与服务'
  elif 'content_commerce' in roles:kind='内容电商'
 row={'id':p['id'],'name':p['displayName'],'tag':p.get('editorialTag') or kind,'path':path,'kind':kind,'directions':p.get('directions',[]),'sources':p.get('sourceLinks',[]),'relationship':'未建立合作','origin':'legacy','date':'2026-10-08','parent':None,'note':'历史公开市场资料；经营角色和当前准入、供货与合作条件仍需逐项核实。'}
 rows.append(row);migration.append({'id':p['id'],'name':p['displayName'],'action':'保留并重新分类','destination':path,'basis':p.get('editorialTag'),'limitations':'不是签约、可调度或已适配通路；历史标签不是经营权限证明。'})
extra=[
 {'id':'sspai','name':'少数派','tag':'数字消费 · 内容与产品共创','path':'creator','kind':'内容推荐','directions':['office','creative','wearable'],'sources':['https://sspai.com/create','https://sspai.com/page/support'],'parent':None,'fact':'官方共创页有产品发布及商务入口；支持页说明内容与销售联盟。','note':'旧联盟页面不能证明任意新品牌准入或可沿用其分佣条件。'},
 {'id':'ifanr','name':'爱范儿','tag':'科技生活 · 图文、视频与直播','path':'creator','kind':'内容推荐','directions':['creative','wearable','home','office'],'sources':['https://www.ifanr.com/adinfo'],'parent':None,'fact':'官方商务页列科技内容、视频直播、社区活动和线下沙龙服务。','note':'内容服务不等于零售采购或成交承诺。'},
 {'id':'smzdm','name':'什么值得买','tag':'兴趣消费 · 内容导购与众测','path':'creator','kind':'内容推荐','directions':['companion','learning','creative','wearable','home','office'],'sources':['https://e.smzdm.com/','https://shangjia.smzdm.com/','https://www.smzdm.com/bangzhu/'],'parent':None,'fact':'官方品牌合作页公开内容种草、用户活动；帮助页有众测与消费社区说明。','note':'不引用其效果数字，不证明联野合作或任意新品活动准入。'},
 {'id':'geekpark','name':'极客公园','tag':'科技内容 · 新品、访谈与活动','path':'creator','kind':'内容推荐','directions':['creative','wearable','office'],'sources':['https://about.geekpark.net/','https://www.geekpark.net/about'],'parent':None,'fact':'官方介绍含新品发布测评、直播、活动与AI产品市集。','note':'专业传播与产品发现，不等于面向终端买家的私域销售。'},
 {'id':'sspai-members','name':'少数派会员社区','tag':'数字生活 · 会员交流与共创','path':'community','kind':'会员社区','directions':['office','creative','wearable'],'sources':['https://sspai.com/community','https://sspai.com/create'],'parent':'少数派','fact':'官方会员社区列选购交流、站内折扣、共创会员周边；共创页有新品发布。','note':'会员场景存在；第三方新品试用、私域触达及销售合作仍需另谈。'},
 {'id':'founderpark','name':'Founder Park','tag':'AI产品人 · 社群与产品市集','path':'community','kind':'专业社群','directions':['office','creative'],'sources':['https://about.geekpark.net/'],'parent':'极客公园','fact':'官方列精细化社群、Workshop与助推冷启动的产品市集。','note':'适合发现与反馈的候选场景，不能视为有消费采购意愿或私域成交能力。'},
 {'id':'ifanr-future','name':'未来社','tag':'科技生活 · 社区活动与沙龙','path':'community','kind':'线下社区','directions':['creative','wearable','home'],'sources':['https://www.ifanr.com/adinfo'],'parent':'爱范儿','fact':'官方商务页列未来社为旗下科技沙龙空间，并公开社区活动服务。','note':'与爱范儿是同一母体下的入口；不单独累计为独立合作主体。'}
]
for r in extra:
 r.update({'origin':'supplement','date':'2026-10-18','relationship':'未建立合作'});rows.append(r)
priority=['智玩店','INNO100','Z·Pilot','AI机器时代','陶朱新造局','博士／总统眼镜','顺电','九机','小米有品','凯知乐','玩具反斗城','三夫户外','Robot Mall']
rows.sort(key=lambda r:priority.index(r['name']) if r['name']in priority else 100)
# Robot Mall's existing tag gives an explicit exhibition/sales context despite its empty legacy role label.
for r in rows:
 if r['name']=='Robot Mall':r['path']='retail';r['kind']='场景展售';r['note']='既有公开来源描述机器人展售与租赁；不代表品牌直成交或我方准入已获确认。'
for item in migration:
 item['destination']=next(r['path'] for r in rows if r['id']==item['id'])
package={'date':'2026-10-18','scope':'公开市场通路与社群入口参考；未建立我方合作','legacyProfiles':len(legacy),'rows':rows}
(root/'data/channels.json').write_text(json.dumps(package,ensure_ascii=False,indent=2))
(root/'data/channels.js').write_text('window.LIANYE_CHANNELS = '+json.dumps(package,ensure_ascii=False).replace('<','\\u003c')+';\n')
(root/'data/migration.json').write_text(json.dumps({'legacyCount':len(legacy),'rows':migration,'supplementEntries':len(extra),'supplementIndependentParents':4,'note':'补充含母体下的会员/社群入口，不可相加当独立伙伴数量；Robot Mall根据展售标签调整到零售。'},ensure_ascii=False,indent=2))
print('legacy',len(legacy),'supplement',len(extra),'total entries',len(rows))
