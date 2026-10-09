"""Research-only structured permission gate; does not interpret legal texts or call AI."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def review(product, proposal):
    issues = []
    evidence_used = []
    if proposal['mode'] == 'resale':
        grant = product.get('grant', {})
        if grant.get('status') != 'confirmed' or not grant.get('evidence'):
            issues.append('resale_permission_unconfirmed')
        else:
            evidence_used.append(grant['evidence'])
            as_of = proposal.get('as_of')
            if grant.get('effective_from') or grant.get('effective_until'):
                if not as_of:
                    issues.append('permission_date_unconfirmed')
                elif (grant.get('effective_from') and as_of < grant['effective_from']) or (grant.get('effective_until') and as_of > grant['effective_until']):
                    issues.append('permission_not_effective_on_proposal_date')
            for dimension in ('product_version', 'region', 'customer_type'):
                if proposal[dimension] not in grant.get(dimension, []):
                    issues.append('resale_scope_mismatch:' + dimension)
    if proposal['deployment'] == 'production_local':
        delivery = product.get('local_delivery', {})
        if delivery.get('status') != 'production_confirmed' or not delivery.get('evidence'):
            issues.append('production_delivery_unconfirmed')
        else:
            evidence_used.append(delivery['evidence'])
    if proposal.get('promises_support'):
        support = product.get('support', {})
        if support.get('status') != 'confirmed' or not support.get('evidence'):
            issues.append('support_responsibility_unconfirmed')
        else:
            evidence_used.append(support['evidence'])
    return {'blocked_claims': issues, 'evidence_used': evidence_used,
            'state': 'claims_blocked' if issues else 'specified_checks_passed',
            'external_use_approved': False,
            'limitations': ['does_not_verify_document_authenticity', 'does_not_determine_channel_interest',
                            'does_not_check_all_commercial_terms', 'human_review_required']}

def main():
    fixture = json.loads((ROOT / 'research/prototype/proposal-permissions-cases-v1.json').read_text())
    results = []
    for case in fixture['cases']:
        result = review(fixture['versions'][case['version']], case['proposal'])
        result['id'] = case['id']
        result['expected_claims_match'] = sorted(result['blocked_claims']) == sorted(case['expected_blocked'])
        results.append(result)
    output = {'scope': fixture['scope'], 'method': 'deterministic_structured_rules_no_ai',
              'results': results, 'all_fixture_expectations_met': all(x['expected_claims_match'] for x in results)}
    target = ROOT / 'research/prototype/proposal-permissions-results-v1.json'
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cases': len(results), 'expectations_met': output['all_fixture_expectations_met'],
                      'business_or_ai_effect_proven': False}, ensure_ascii=False))
    if not output['all_fixture_expectations_met']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
