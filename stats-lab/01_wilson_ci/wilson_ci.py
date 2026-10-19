from math import sqrt

def wilson_ci(successes, n, z=1.96):
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("Invalid counts")

    p = successes / n
    d = 1 + z**2 / n

    center = (p + z**2 / (2 * n)) / d
    margin = (
        z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    ) / d

    return center - margin, center + margin


print("=== WILSON 95% CONFIDENCE INTERVALS ===")

widths = []

for n in (20, 100, 500):
    correct = int(n * 0.80)
    low, high = wilson_ci(correct, n)
    widths.append(high - low)

    print(
        f"n={n:3d} | "
        f"accuracy={100 * correct / n:.1f}% | "
        f"95% CI=[{100 * low:.1f}%, {100 * high:.1f}%]"
    )

assert widths[0] > widths[1] > widths[2]
print("RESULT: PASS")