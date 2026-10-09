"""Literal warning baseline; flags explicit words, does not infer cross-document change."""
import json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'research/prototype'
source=p/'material-change-input-v1.json'; x=json.loads(source.read_text())
terms={'exclusion':'不包含','separate_price':'单独报价','delay':'延迟','unknown_date':'尚未确定','unpublished_policy':'未公开'}
rows=[]
for case in x['cases']:
 flags=[]
 for material in case['materials']:
  for kind,term in terms.items():
   if term in material['text']:flags.append({'kind':kind,'literal':term,'materialId':material['id'],'providedText':material['text']})
 rows.append({'caseId':case['id'],'flags':flags,'decision':'human_review_required','crossDocumentMeaningEstablished':False,'purchaseFitEstablished':False})
out={'method':'literal_warning_rules','inputSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':rows,'limits':'固定词表是弱基线；只定位显式提醒，不证明语义关系，不代表完善规则系统能力。无工时及真实结果对照。'}
(p/'material-change-rule-output-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Literal flags saved for three hypothetical material cases; no semantic or commercial success inferred.')
