"""Deterministic decisions after HUMAN normalization; no semantic/AI efficacy claim."""
import json,datetime,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'research/prototype'
p=root/'feedback-structured-events-v1.json';packet=json.loads(p.read_text());raw=json.loads((root/packet['rawInput']).read_text());sources={(c['id'],f['id']):f['text'] for c in raw['cases'] for f in c['feedback']};out=[]
for e in packet['events']:
 key=(e['caseId'],e['feedbackId']);assert key in sources
 kind=e['kind'];d={'caseId':key[0],'feedbackId':key[1],'sourceText':sources[key],'scope':e['scope'],'humanNormalized':True,'automaticOutreachAllowed':False}
 if kind=='local_constraint':d.update(status='local_constraint',nextAction='verify_other_actors_or_later_conditions')
 elif kind=='requirements':d.update(status='pending_requirements',nextAction='confirm_and_prepare_required_documents',requirements=e['requirements'])
 elif kind=='deadline':
  conflict=datetime.date.fromisoformat(e['availableSaleableDate'])>datetime.date.fromisoformat(e['requiresSaleableDate'])
  d.update(status='deadline_conflict' if conflict else 'date_condition_satisfied_only',nextAction='reconsider_activity_date' if conflict else 'confirm_remaining_conditions',demoSeparateFromSaleable=True)
 elif kind=='no_reply':d.update(status='awaiting_reply',nextAction='retain_unknown_opinion')
 elif kind=='not_received':d.update(status='new_version_not_received',nextAction='human_confirm_before_send')
 elif kind=='version_update':d.update(status='documents_updated_not_accepted',nextAction='request_actor_reassessment',providedDocuments=e['providedDocuments'],acceptedDocuments=e['acceptedDocuments'],unresolved=e['unresolved'])
 else:raise ValueError(kind)
 out.append(d)
result={'scope':'rules_after_manual_structuring_not_equal_cost_comparison','structuredInputSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'events':out,'limits':['人工结构化未计时','不解释原始语义','不合并采购许可与转售许可','不证明采购或业务效果']}
(root/'feedback-structured-rule-output-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f'{len(out)} evidence-linked events processed; no automatic outreach')
