#!/usr/bin/env python3
"""Read-only, post-run technical verification of M5-H12 evidence.

Scope: verifies consistency of submitted JSON and pre-authored frozen case file;
does not establish independent precommitment, original integration ZIP identity,
or recreate actual model/host runtime.
Python standard library only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

EXPECTED_ARCHIVE_SHA256 = 'e0fd85dbed3b1b605fc2fecfc1c1c425727b89f6beae102b0254b86b0e38a15c'
EXPECTED_CASES_SHA256 = '4ad7adf13c6d93543fac09d05221f0737c15810b5d7a77e2044e0f947b35a86a'
EXPECTED_BASE_ZIP_SHA256 = '93b9380680f67efca72ee579122552b8b3cb8c00617224435b6741b2e74cf2b5'


def sha(buf: bytes) -> str:
    return hashlib.sha256(buf).hexdigest()


def can(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def strict_json(raw: bytes):
    def hook(items):
        d = {}
        for k, v in items:
            if k in d:
                raise AssertionError('duplicate JSON key: ' + k)
            d[k] = v
        return d
    return json.loads(raw.decode('utf-8'), object_pairs_hook=hook)


def check(ok, message):
    if not ok:
        raise AssertionError(message)


def model_view(req):
    return {
        'attestation_payload': req['attestation_payload'],
        'binding': req['binding'],
        'lifecycle_events': [
            {'event_type': e['event_type'], 'observed_at': e['observed_at']}
            for e in req['lifecycle_events']
        ]
    }


def verify(evidence_path: Path, frozen_file: Path | None) -> dict:
    check(evidence_path.is_file(), 'missing evidence ZIP')
    check(sha(evidence_path.read_bytes()) == EXPECTED_ARCHIVE_SHA256, 'Evidence ZIP SHA-256 mismatch')
    names = [f'CASE_H12-{x:02d}.json' for x in range(1, 13)] + [
        'FINAL_STATUS.json', 'PREREGISTRATION_SNAPSHOT.json'
    ]
    with zipfile.ZipFile(evidence_path) as z:
        check(z.testzip() is None, 'ZIP CRC validation failed')
        check(len(z.namelist()) == 14 and set(z.namelist()) == set(names), 'Unexpected ZIP entries')
        check(all(not x.is_dir() for x in z.infolist()), 'Unexpected directory in ZIP')
        objects = {name: strict_json(z.read(name)) for name in names}

    snap = objects['PREREGISTRATION_SNAPSHOT.json']
    status = objects['FINAL_STATUS.json']
    frozen = snap['frozen_cases']
    cases = frozen['cases']
    check(snap['archive_sha256'] == EXPECTED_BASE_ZIP_SHA256, 'Declared integration ZIP hash mismatch')
    check(snap['original_frozen_cases_and_oracle_sha256'] == EXPECTED_CASES_SHA256,
          'Frozen source hash claim mismatch')
    check(len(cases) == 12, 'Wrong number of preregistered cases')
    check([c['case_id'] for c in cases] == [f'H12-{x:02d}' for x in range(1, 13)], 'Case IDs changed')
    check(len(snap.get('source_modules', [])) == 10, 'Source module provenance incomplete')
    check(snap['model'] == 'qwen3:0.6b' and snap['temperature'] == 0 and snap['seed'] == 20261025,
          'Unexpected model settings in snapshot')
    if frozen_file is not None:
        check(frozen_file.is_file(), 'Frozen source file missing')
        check(sha(frozen_file.read_bytes()) == EXPECTED_CASES_SHA256, 'Frozen source file hash mismatch')
        check(strict_json(frozen_file.read_bytes()) == frozen, 'Frozen source differs from snapshot')

    gate_reasons, paired_diag = {}, {'both_correct': 0, 'A_only': 0, 'B_only': 0, 'both_wrong': 0}
    counts = {
        'model_A_correct': 0, 'host_B_correct': 0,
        'model_A_false_allow': 0, 'model_A_false_stop': 0,
        'host_B_false_allow': 0, 'host_B_false_stop': 0,
        'model_A_invalid_or_unresolved': 0, 'host_B_inconclusive': 0,
    }
    detail = []
    reference_counts = {'HOST_ALLOW': 0, 'HOST_STOP': 0}
    expected_policy = {
        'max_age_days': 30, 'require_purpose_match': True, 'require_audience_match': True,
        'require_resource_match': True, 'require_revocation_known': True,
        'block_revoked': True, 'block_failed_mandatory_reverify': True,
        'block_superseded_target': True, 'unresolved_on_active_conflict': True,
    }
    for item in cases:
        cid, gold, full_req = item['case_id'], item['reference'], item['request']
        check(gold in reference_counts, 'Unexpected oracle decision')
        reference_counts[gold] += 1
        row = objects[f'CASE_{cid}.json']
        check(row['case_id'] == cid and row['reference'] == gold, 'Case/reference mismatch')
        check(row['full_request_sha256'] == sha(can(full_req)), 'Request hash mismatch: ' + cid)
        check(row['model_view_sha256'] == sha(can(model_view(full_req))), 'Model view hash mismatch: ' + cid)
        check(row['A_observed'] is True and row['B_observed'] is True, 'Incomplete case: ' + cid)
        a_req, a_out, b_out = row['A_request'], row['A_raw_response'], row['B_raw_response']
        prompt = a_req['prompt']
        check(row['A_prompt_sha256'] == sha(prompt.encode('utf-8')), 'Prompt hash mismatch: ' + cid)
        check(a_req['model'] == 'qwen3:0.6b' and a_req['stream'] is False and a_req['think'] is False,
              'Unexpected model API fields: ' + cid)
        check(a_req['options'] == {'num_predict': 128, 'seed': 20261025, 'temperature': 0},
              'Unexpected model options: ' + cid)
        check(a_out['model'] == a_req['model'] and a_out.get('done') is True,
              'Model execution metadata mismatch: ' + cid)
        check(a_out['response'] == row['A_label'], 'Raw Qwen answer differs from recorded label: ' + cid)
        check(row['A_label'] in {'HOST_ALLOW', 'HOST_STOP', 'HOST_UNRESOLVED'},
              'Unexpected raw Qwen label: ' + cid)
        check('"reference"' not in prompt and '"request_id"' not in prompt
              and '"anchor_projection"' not in prompt and item['reference_rationale'] not in prompt,
              'Oracle/label leaked to prompt: ' + cid)
        check(full_req['request_id'] not in prompt, 'Request ID leaked to model: ' + cid)
        check('POLICY_JSON:\n' in prompt and '\n\nCASE_JSON:\n' in prompt,
              'Prompt sections missing: ' + cid)
        policy_text = prompt.split('POLICY_JSON:\n', 1)[1].split('\n\nCASE_JSON:\n', 1)[0]
        case_text = prompt.split('\n\nCASE_JSON:\n', 1)[1].strip()
        check(strict_json(policy_text.encode('utf-8')) == expected_policy,
              'Policy in prompt differs: ' + cid)
        check(strict_json(case_text.encode('utf-8')) == model_view(full_req),
              'Model facts differ from preregistration: ' + cid)
        check(b_out['request_id'] == full_req['request_id'], 'B request identity mismatch: ' + cid)
        check(b_out['anchor_identity'].get('kind') == 'HOST_GATE_PROBE_NO_ANCHOR',
              'B probe not marked as no Anchor: ' + cid)
        check(b_out['final_action_authorized'] is False,
              'Unexpected final authorization: ' + cid)
        check(b_out['lifecycle_policy_version'] == 'host-policy:0.5.0',
              'Wrong host policy version: ' + cid)
        calls = row['B_callback_calls']
        if row['B_gate_label'] == 'HOST_STOP':
            check(gold == 'HOST_STOP', 'Unexpected B stop vs prereg: ' + cid)
            check(calls == 0 and b_out['decision'] == 'STOP'
                  and b_out['source'] == 'HOST_POLICY' and b_out['anchor_called'] is False,
                  'B stop trace mismatch: ' + cid)
            for reason in b_out['reason_codes']:
                gate_reasons[reason] = gate_reasons.get(reason, 0) + 1
        elif row['B_gate_label'] == 'HOST_ALLOW':
            check(calls == 1 and b_out['decision'] == 'STOP'
                  and b_out['source'] == 'PILOT_RUNTIME' and b_out['anchor_called'] is True,
                  'B allow-to-callback trace mismatch: ' + cid)
            check('ANCHOR_OR_RUNTIME_EXECUTION_ERROR' in b_out['reason_codes'],
                  'B probe exception reason missing: ' + cid)
        else:
            raise AssertionError('Unexpected B label: ' + cid)
        a, b = row['A_label'], row['B_gate_label']
        counts['model_A_correct'] += a == gold
        counts['host_B_correct'] += b == gold
        counts['model_A_false_allow'] += gold == 'HOST_STOP' and a == 'HOST_ALLOW'
        counts['model_A_false_stop'] += gold == 'HOST_ALLOW' and a == 'HOST_STOP'
        counts['host_B_false_allow'] += gold == 'HOST_STOP' and b == 'HOST_ALLOW'
        counts['host_B_false_stop'] += gold == 'HOST_ALLOW' and b == 'HOST_STOP'
        counts['model_A_invalid_or_unresolved'] += a in ('INVALID_OUTPUT', 'HOST_UNRESOLVED')
        counts['host_B_inconclusive'] += b == 'INCONCLUSIVE'
        pair_label = ('both_correct' if a == gold and b == gold else
                      'A_only' if a == gold else
                      'B_only' if b == gold else 'both_wrong')
        paired_diag[pair_label] += 1
        detail.append({'case_id': cid, 'reference': gold, 'A_Qwen': a,
                       'B_host_gate': b, 'B_callback_calls': calls,
                       'B_wire_decision': b_out['decision'],
                       'B_wire_source': b_out['source'],
                       'B_reason_codes': b_out['reason_codes'],
                       'pair': pair_label, 'reference_rationale': item['reference_rationale']})
    check(reference_counts == {'HOST_ALLOW': 6, 'HOST_STOP': 6}, 'Unexpected oracle balance')
    recorded_scores = status['scores']
    check(status['raw_case_files'] == [f'CASE_H12-{x:02d}.json' for x in range(1, 13)],
          'FINAL_STATUS file list mismatch')
    check(recorded_scores['status'] == 'COMPLETE_12_PAIRED'
          and recorded_scores['cases_with_both_observed'] == 12, 'Execution status mismatch')
    check(recorded_scores['fair_full_CFC_AB'] == 'NOT_ESTABLISHED'
          and recorded_scores['frozen_anchor_executed'] is False,
          'Full Anchor status inconsistent')
    for key, val in counts.items():
        check(recorded_scores[key] == val, 'Score mismatch: ' + key)
    check(reference_counts == status['predeclared_reference'], 'FINAL_STATUS reference mismatch')
    return {
        'audit_type': 'POST_RUN_INTERNAL_TECHNICAL_CONSISTENCY_CHECK',
        'status': 'PASS_WITH_SCOPE_LIMITATIONS',
        'evidence_archive': evidence_path.name,
        'evidence_zip_sha256': EXPECTED_ARCHIVE_SHA256,
        'source_preregistered_file_sha256': EXPECTED_CASES_SHA256,
        'source_frozen_file_crosscheck': frozen_file is not None,
        'source_integration_zip_sha256_reported_not_independently_rehashed': EXPECTED_BASE_ZIP_SHA256,
        'count_files': 14,
        'cases': 12,
        'reference_counts': reference_counts,
        'score_recomputed': counts,
        'paired_outcomes': paired_diag,
        'host_stop_reason_codes': gate_reasons,
        'case_details': detail,
        'interpretation_limits': [
            'Not an independent external review: dataset, harness and post-run audit are from the same collaboration.',
            'Archived self-authored frozen data match preregistered source; not an independently timestamped preregistration.',
            'Original integration ZIP was verified by original Windows harness per its code/logs, but is not included here for direct rehash.',
            'No frozen Anchor, HAWM, downstream enforcement or production decision executed.',
            'Cases deliberately balanced, synthetic and tied to the same deterministic contract; no population-level accuracy inference.',
            'B=HOST_ALLOW denotes callback reachability, not final authorization; B wire STOP/PILOT_RUNTIME intentional.',
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('evidence_zip', type=Path)
    ap.add_argument('--frozen-file', type=Path, default=None)
    ap.add_argument('--json-output', type=Path)
    args = ap.parse_args()
    result = verify(args.evidence_zip, args.frozen_file)
    if args.json_output:
        args.json_output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')
    print(result['status'], result['score_recomputed'], result['paired_outcomes'])


if __name__ == '__main__':
    main()