# AI Evaluation & Assurance Portfolio

**Krzysztof Sliwka** · [GitHub @iller1](https://github.com/iller1)

A portfolio of small, inspectable studies in AI evaluation, experimental design, and evidence-based assurance. Findings are published even when they do **not** support the tested improvement. This repository is separate from the [CFC project](https://github.com/iller1/cfc-ai-evaluation).

## Study 01 — Does a careful-comparison instruction improve Qwen3-0.6B accuracy?

- **Date:** 19 October 2026
- **Setup:** one Qwen3-0.6B model (Ollama 0.40.5), 200 paired questions from the ARC-Easy test split; 400 recorded responses; constrained JSON answer labels.
- **Variant A:** baseline selection instruction, **161/200 (80.5%)**.
- **Variant B:** instruction to compare every option carefully, **157/200 (78.5%)**.
- **Paired effect (B − A): −2.0 percentage points**; exact two-sided McNemar **p = 0.38769531**; paired percentile bootstrap 95% CI **[−5.5, +1.5] percentage points**.
- **Interpretation:** no statistically established improvement. This is **not** proof of equivalent performance, and does not establish that A is universally better.

**[Read the five-page study PDF](reports/report_01/Report01_Qwen3_ARC_Easy_Evaluation_EN.pdf)** · **[Methods, evidence boundaries and instructions](reports/report_01/README.md)** · **[External reviewer checklist](reports/report_01/REVIEWER_CHECKLIST.md)**

### Reproduce the published statistical calculations

Python 3.9+; Python standard library only; no account, model download or API key needed.

```bash
python reports/report_01/recompute_paired_statistics.py reports/report_01/paired_outcomes_200.csv
```

Expected: `RESULT: PASS`, paired counts (both correct 153, A-only 8, B-only 4, both wrong 35) and the results above.

**Reproduction boundary:** the public CSV contains **derived 0/1 outcomes, not original questions, prompts or raw model responses**. The script recomputes statistics and verifies the published CSV checksum; it **does not** independently verify model execution or answer scoring. The complete original evidence was checked locally and is retained separately, subject to a privacy/licensing review before any disclosure. No external independent validation or custody is claimed.

## Study 02

Planned under the portfolio schedule; **not yet conducted or published**. No results are claimed.

## Data attribution and rights

Study 01 evaluates the **AI2 ARC / ARC-Easy** benchmark (Clark et al., 2018): [dataset](https://huggingface.co/datasets/allenai/ai2_arc) · [paper](https://arxiv.org/abs/1803.05457). The dataset card specifies **CC BY-SA 4.0**. No original benchmark question text is redistributed in this repository.

No repository-wide reuse license has been granted yet for the author's own material; see source licenses for third-party resources. Any external assessment should state exactly what it checked rather than using an unqualified “independently verified” claim.
