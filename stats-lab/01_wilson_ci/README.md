# Statistics Lab 01 — Wilson Confidence Intervals

## Research question

How does sample size affect uncertainty when the observed accuracy stays at 80%?

## Method

Calculate approximate 95% Wilson score confidence intervals for three illustrative binomial samples.

| Correct | Sample size | Accuracy | 95% Wilson CI |
|---|---:|---:|---|
| 16 | 20 | 80.0% | 58.4%–91.9% |
| 80 | 100 | 80.0% | 71.1%–86.7% |
| 400 | 500 | 80.0% | 76.3%–83.3% |

## Reproduce

Run:

```powershell
python wilson_ci.py
```

Expected result: RESULT: PASS.

## Interpretation

All three observed accuracies are identical, but interval width decreases as sample size increases.

A 95% frequentist confidence interval does not mean there is a 95% probability that the fixed parameter lies inside this particular computed interval.

## Assumptions and limitations

- Data are illustrative counts, not new model measurements.
- The calculation assumes independent binary observations under a stable success probability.
- Biased sampling, correlated observations, and distribution shifts can invalidate the intended interpretation.
- A narrower interval does not establish that the evaluation dataset represents all real-world use cases.

## Status

COMPLETED — educational statistical exercise.
No external validation is claimed.