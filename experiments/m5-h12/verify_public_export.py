#!/usr/bin/env python3
"""Audit the 14 verbatim JSON members of M5-H12's public text export.

Python stdlib only. Rebuilds a *temporary*, non-byte-identical ZIP and reuses the
post-run consistency verifier. This does not independently witness an execution,
verify the original ZIP's byte checksum, or run CFC/Anchor/HAWM.
"""
import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

import verify_evidence


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('export', type=Path)
    p.add_argument('--frozen-file', type=Path, required=True)
    args = p.parse_args()
    export = json.loads(args.export.read_text(encoding='utf-8'))
    assert export['schema'] == 'M5_H12_PUBLIC_EVIDENCE_EXPORT_V1'
    assert export['original_zip_sha256'] == verify_evidence.EXPECTED_ARCHIVE_SHA256
    records = export['original_member_utf8_contents']
    hashes = export['sha256_of_original_member_bytes']
    expected = {f'CASE_H12-{i:02d}.json' for i in range(1,13)} | {'PREREGISTRATION_SNAPSHOT.json', 'FINAL_STATUS.json'}
    assert set(records) == set(hashes) == expected, 'Missing, extra or duplicate archive entries'
    payload = {}
    for name, text in records.items():
        raw = text.encode('utf-8')
        assert sha(raw) == hashes[name], f'Member SHA mismatch: {name}'
        payload[name] = raw
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'reconstructed_for_audit_only.zip'
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name in sorted(payload):
                z.writestr(name, payload[name])
        verify_evidence.EXPECTED_ARCHIVE_SHA256 = sha(path.read_bytes())
        result = verify_evidence.verify(path, args.frozen_file)
    print('PUBLIC_EXPORT_AUDIT:', result['status'])
    print('VERBATIM_JSON_MEMBERS:', len(payload))
    print('RECOMPUTED_SCORES:', json.dumps(result['score_recomputed'], sort_keys=True))
    print('PAIRED_OUTCOMES:', json.dumps(result['paired_outcomes'], sort_keys=True))
    print('ORIGINAL_ZIP_BYTES: NOT_REVERIFIED (members only; ZIP container differs)')
    print('FROZEN_ANCHOR: NOT_EXECUTED')


if __name__ == '__main__':
    main()
