"""Audit populated, attributed operating fields; never infer commercial readiness."""
import json
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]
base=root/'research/current'
profiles=json.loads((base/'channel-asset.json').read_text())['profiles']
fields=['buyerScenarios','productScope','regions','entryPoints','deliveryRequirements','afterSalesRequirements']
names={'companion':'陪伴与亲子','learning':'学习与教育','wearable':'运动与穿戴','home':'家庭与空间','office':'办公与生产力','creative':'创作与数码'}
reviewed=lambda p: bool(p.get('fieldEvidence'))
counts={f:sum(bool(p.get(f)) and bool(p.get('fieldEvidence',{}).get(f)) for p in profiles) for f in fields}
result={'scope':'research_depth_not_partner_count','profiles':len(profiles),'reviewedProfiles':sum(reviewed(p) for p in profiles),'attributedNonemptyFields':counts,'directions':{},'limits':'字段有来源不等于准入已核实；品牌目录入口不等于新品供应商入口；分类仍为编辑判断。','stage1Complete':False}
lines=['# 经营信息覆盖复查','', '基于当前渠道资产自动生成，数量仅用于内部研究，不进入官网。逐字段有来源仍不能证明合作意愿、采购权限或我方承接能力。','', '|产品方向|档案|部分字段有来源|买家场景|产品范围|区域|入口|交付|售后|','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for key,title in names.items():
 rows=[p for p in profiles if key in p['directions']]
 c={f:sum(bool(p.get(f)) and bool(p.get('fieldEvidence',{}).get(f)) for p in rows) for f in fields}
 result['directions'][key]={'profiles':len(rows),'partiallyReviewed':sum(reviewed(p) for p in rows),'fields':c}
 lines.append('|'+title+'|'+ '|'.join(map(str,[len(rows),sum(reviewed(p) for p in rows),*c.values()]))+'|')
lines+=['','## 不能被总数掩盖的缺口','','运动方向增加了同一品牌官方目录的经营者信息，证明的是指定品牌销售范围，不是任意AI穿戴的采购能力。下一步不继续靠同一目录扩大体量。','','陪伴方向仍缺玩具及互动电子产品经营者的经营条件；学习方向要区分教育品牌销售与学校项目交付；家庭方向要区分安装集成和独立设备销售；办公方向需核实软件授权、部署与服务责任；创作方向要补音频以外的软件及创作者工具通路。','','## 使用方式','','有来源的范围用于初步讨论对象筛选；入口用于确认从哪里核实；交付与售后字段用于识别需要补问的条件。未知项必须保留。没有获授权项目记录与结果口径前，不生成成功概率、销量预测或规模化复制结论。']
(base/'depth-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(base/'operating-coverage-review.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
