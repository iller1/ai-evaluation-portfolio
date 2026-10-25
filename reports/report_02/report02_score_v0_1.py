#!/usr/bin/env python3
"""Report #2: prespecified cross-seed agreement scorer (standard library only).

Final response records (JSONL), exactly one per case and pass:
  {"case_id":"MAIN-001","pass_id":"A","seed":101,
   "transport_ok":true,"response_text":"{\"label\":\"SUPPORTED\"}"}

response_text is the exact string returned in Ollama's `response` field.
Full unmodified API requests/responses and retry attempts must be preserved
separately by the runner; this scorer does not replace those raw receipts.
Reference labels are NEVER used to score cross-seed agreement.

Usage (after main run):
  python report02_score_v0_1.py --contract model_contract_v0_1_REVIEW.json \\
      --dataset main_dataset_45_v0_2_REVIEW.json --results final_responses.jsonl \\
      --output scoring_summary.json

Before main run:
  python report02_score_v0_1.py --self-test
"""

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

LABELS = ("SUPPORTED", "CONTRADICTED", "NOT_ESTABLISHED")
RECORD_KEYS = {"case_id", "pass_id", "seed", "transport_ok", "response_text"}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def no_duplicate_object_keys(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError(f"Duplicate JSON key: {k}")
        obj[k] = v
    return obj


def reject_nonfinite(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def strict_label(response_text):
    """A valid classification is a JSON object with exactly one valid label."""
    if not isinstance(response_text, str):
        return None
    try:
        obj = json.loads(
            response_text,
            object_pairs_hook=no_duplicate_object_keys,
            parse_constant=reject_nonfinite,
        )
    except (ValueError, TypeError):
        return None
    if not isinstance(obj, dict) or set(obj) != {"label"}:
        return None
    label = obj["label"]
    return label if isinstance(label, str) and label in LABELS else None


def summarize(dataset, contract, final_records):
    """Score complete case-pass records, with strict integrity checks."""
    summary = {"decision": "INCONCLUSIVE", "reason": None}
    if not isinstance(dataset, list) or len(dataset) != 45:
        summary["reason"] = "Dataset must contain exactly 45 records"
        return summary
    try:
        case_ids = [case["id"] for case in dataset]
        if len(set(case_ids)) != 45 or any(not isinstance(i, str) for i in case_ids):
            raise ValueError("Duplicate or invalid case IDs")
        if not isinstance(final_records, list):
            raise ValueError("Final records must be a list")
        passes = contract["passes"]
        seeds = {p["id"]: p["seed"] for p in passes}
        if seeds != {"A": 101, "B": 202} or len(passes) != 2:
            raise ValueError("Unexpected pass/seed design")
        scoring = contract["scoring"]
        assert scoring["primary_denominator"] == 45
        assert scoring["invalid_output_counts_as_nonmatch"] is True
        assert scoring["kappa_population"] == "both_valid_pairs_only"
        assert scoring["minimum_valid_pairs"] == 43
        assert scoring["minimum_matching_valid_pairs"] == 40
        assert scoring["minimum_kappa"] == 0.70
    except (KeyError, ValueError, TypeError, AssertionError) as exc:
        summary["reason"] = f"Contract/data integrity problem: {exc}"
        return summary

    known = set(case_ids)
    indexed = {}
    for idx, r in enumerate(final_records, 1):
        if not isinstance(r, dict) or set(r) != RECORD_KEYS:
            summary["reason"] = f"Invalid final record schema at line {idx}"
            return summary
        cid, pid, seed = r["case_id"], r["pass_id"], r["seed"]
        if not isinstance(cid, str) or cid not in known or pid not in seeds:
            summary["reason"] = f"Unknown case or pass at line {idx}"
            return summary
        if type(seed) is not int or seed != seeds[pid]:
            summary["reason"] = f"Unexpected seed at line {idx}"
            return summary
        if type(r["transport_ok"]) is not bool:
            summary["reason"] = f"Invalid transport status at line {idx}"
            return summary
        if not isinstance(r["response_text"], str) and r["response_text"] is not None:
            summary["reason"] = f"Invalid response text type at line {idx}"
            return summary
        key = (cid, pid)
        if key in indexed:
            summary["reason"] = f"Duplicate result for {cid}/{pid}"
            return summary
        indexed[key] = r

    expected = {(cid, p) for cid in case_ids for p in seeds}
    missing = expected - set(indexed)
    if missing:
        summary["decision"] = "NOT_READY"
        summary["reason"] = f"Missing {len(missing)} of 90 final case-pass records"
        summary["recorded"] = len(indexed)
        return summary

    bad_transports = [key for key, r in indexed.items() if not r["transport_ok"]]
    if bad_transports:
        summary["reason"] = f"Unresolved transport failures: {len(bad_transports)}"
        return summary

    invalid_per_pass = {"A": 0, "B": 0}
    valid_pairs = 0
    matched_pairs = 0
    counts_a = Counter()
    counts_b = Counter()
    table = {a: {b: 0 for b in LABELS} for a in LABELS}
    mismatches = []
    invalid_pairs = []
    for cid in case_ids:
        a = strict_label(indexed[(cid, "A")]["response_text"])
        b = strict_label(indexed[(cid, "B")]["response_text"])
        if a is None:
            invalid_per_pass["A"] += 1
        if b is None:
            invalid_per_pass["B"] += 1
        if a is None or b is None:
            invalid_pairs.append(cid)
            continue
        valid_pairs += 1
        counts_a[a] += 1
        counts_b[b] += 1
        table[a][b] += 1
        if a == b:
            matched_pairs += 1
        else:
            mismatches.append({"case_id": cid, "A": a, "B": b})

    p_observed = matched_pairs / valid_pairs if valid_pairs else None
    p_expected = (
        sum(counts_a[label] * counts_b[label] for label in LABELS) / valid_pairs ** 2
        if valid_pairs else None
    )
    kappa = (
        (p_observed - p_expected) / (1 - p_expected)
        if valid_pairs and not math.isclose(p_expected, 1.0, abs_tol=1e-12) else None
    )
    summary.update({
        "records": 90,
        "case_pairs": 45,
        "both_valid_pairs": valid_pairs,
        "invalid_per_pass": invalid_per_pass,
        "invalid_pair_ids": invalid_pairs,
        "matching_valid_pairs": matched_pairs,
        "strict_agreement_all_45": matched_pairs / 45,
        "observed_agreement_both_valid": p_observed,
        "expected_agreement_both_valid": p_expected,
        "cohens_kappa_both_valid": kappa,
        "contingency_A_rows_B_columns": table,
        "disagreements": mismatches,
        "thresholds": {
            "minimum_valid_pairs": 43,
            "minimum_matching_valid_pairs": 40,
            "minimum_kappa": 0.70,
        },
    })
    passed = (valid_pairs >= 43 and matched_pairs >= 40
              and kappa is not None and kappa >= 0.70)
    summary["decision"] = "PASS" if passed else "FAIL"
    summary["reason"] = "Prespecified pilot thresholds met" if passed else "One or more prespecified pilot thresholds not met"
    return summary


def self_test():
    dataset = [{"id": f"MAIN-{i:03}"} for i in range(1, 46)]
    contract = {
        "passes": [{"id": "A", "seed": 101}, {"id": "B", "seed": 202}],
        "scoring": {
            "primary_denominator": 45,
            "invalid_output_counts_as_nonmatch": True,
            "kappa_population": "both_valid_pairs_only",
            "minimum_valid_pairs": 43,
            "minimum_matching_valid_pairs": 40,
            "minimum_kappa": 0.70,
        },
    }
    records = []
    for i in range(1, 46):
        label = LABELS[(i - 1) % 3]
        for pid, seed in (("A", 101), ("B", 202)):
            records.append({"case_id": f"MAIN-{i:03}", "pass_id": pid,
                            "seed": seed, "transport_ok": True,
                            "response_text": json.dumps({"label": label})})

    assert summarize(dataset, contract, records)["decision"] == "PASS"
    print("TEST 1: exact matching, balanced labels => PASS")

    broken = [dict(x) for x in records]
    broken[1]["response_text"] = '{"label":"SUPPORTED","extra":42}'
    score = summarize(dataset, contract, broken)
    assert score["decision"] == "PASS" and score["invalid_per_pass"]["B"] == 1
    assert score["matching_valid_pairs"] == 44
    print("TEST 2: invalid output counts as a nonmatching pair => PASS")

    broken = [dict(x) for x in records]
    for i in range(1, 46, 2):
        broken[i]["response_text"] = '{"label":"INVALID"}'
    assert summarize(dataset, contract, broken)["decision"] == "FAIL"
    print("TEST 3: many invalid outputs => FAIL")

    assert summarize(dataset, contract, records[:-1])["decision"] == "NOT_READY"
    print("TEST 4: missing final result => NOT_READY")

    broken = records + [dict(records[0])]
    assert summarize(dataset, contract, broken)["decision"] == "INCONCLUSIVE"
    print("TEST 5: duplicate final record => INCONCLUSIVE")

    broken = [dict(x) for x in records]
    broken[0]["seed"] = 202
    assert summarize(dataset, contract, broken)["decision"] == "INCONCLUSIVE"
    print("TEST 6: wrong seed => INCONCLUSIVE")

    broken = [dict(x) for x in records]
    broken[0]["transport_ok"] = False
    broken[0]["response_text"] = None
    assert summarize(dataset, contract, broken)["decision"] == "INCONCLUSIVE"
    print("TEST 7: unresolved transport failure => INCONCLUSIVE")

    broken = [dict(x) for x in records]
    for x in broken:
        x["response_text"] = '{"label":"SUPPORTED"}'
    score = summarize(dataset, contract, broken)
    assert score["decision"] == "FAIL" and score["cohens_kappa_both_valid"] is None
    print("TEST 8: undefined kappa => FAIL")

    assert strict_label('{"label":"SUPPORTED","label":"CONTRADICTED"}') is None
    assert strict_label('{"label": "SUPPORTED"}') == "SUPPORTED"
    assert strict_label('not json') is None
    assert strict_label(' {"label":"SUPPORTED"} ') == "SUPPORTED"
    print("TEST 9: strict JSON validation => PASS")

    print("RESULT: SCORER SELF-TEST 9/9 PASS (NO MODEL CALLS)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.contract or not args.dataset or not args.results:
        parser.error("Specify --self-test OR --contract, --dataset, and --results")

    contract_raw = args.contract.read_bytes()
    contract = json.loads(contract_raw.decode("utf-8"))
    dataset_raw = args.dataset.read_bytes()
    if sha256(dataset_raw) != contract["dataset_sha256"]:
        raise SystemExit("INCONCLUSIVE: dataset SHA256 does not match contract")
    if args.dataset.name != contract["dataset_file"]:
        raise SystemExit("INCONCLUSIVE: dataset file name does not match contract")
    dataset = json.loads(dataset_raw.decode("utf-8"))
    results_raw = args.results.read_bytes()
    try:
        final_records = [json.loads(line, object_pairs_hook=no_duplicate_object_keys,
                                    parse_constant=reject_nonfinite)
                         for line in results_raw.decode("utf-8").splitlines() if line.strip()]
    except ValueError as exc:
        final_records = None
        parse_error = str(exc)
    else:
        parse_error = None
    if parse_error:
        result = {"decision": "INCONCLUSIVE", "reason": f"Malformed result log: {parse_error}"}
    else:
        result = summarize(dataset, contract, final_records)

    result.update({
        "contract_sha256": sha256(contract_raw),
        "dataset_sha256": sha256(dataset_raw),
        "final_results_sha256": sha256(results_raw),
        "reference_labels_used_for_scoring": False,
        "limitations": "Cross-seed stability on 45 author-created examples; not accuracy or generalization",
    })
    content = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(content)
    if args.output:
        with args.output.open("x", encoding="utf-8") as fh:
            fh.write(content)
        print("SUMMARY SAVED:", args.output)


if __name__ == "__main__":
    main()
