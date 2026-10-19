#!/usr/bin/env python3
"""Recompute Report 01 paired statistics on the *derived* public outcomes.

This does not verify model outputs, sample choice, response authenticity, or hashes
of the original evidence archive. Python standard library only, no networking.
"""
import csv
import hashlib
import math
import random
import sys
from collections import Counter
from pathlib import Path

EXPECTED_SHA256 = "b4cbfd239b236f0719d1805d6e68aa079b52ff3aa9abffdddf4556b1158fa267"


def percentile(values, p):
    position=(len(values)-1)*p
    lo=math.floor(position); hi=math.ceil(position)
    return values[lo]+(position-lo)*(values[hi]-values[lo])


def main(csvpath):
    raw=csvpath.read_bytes()
    got=hashlib.sha256(raw).hexdigest()
    if got!=EXPECTED_SHA256:
        raise ValueError('CSV SHA-256 does not match this release')
    with csvpath.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames != ['pair_index','A_correct','B_correct']:
            raise ValueError('Unexpected columns')
        records=list(reader)
    if len(records)!=200:
        raise ValueError('Expected 200 complete pairs')
    pairs=[]
    for i,row in enumerate(records,1):
        if row['pair_index']!=str(i) or row['A_correct'] not in ('0','1') or row['B_correct'] not in ('0','1'):
            raise ValueError(f'Invalid row {i}')
        pairs.append((int(row['A_correct']),int(row['B_correct'])))
    c=Counter(pairs)
    A=sum(a for a,b in pairs)
    B=sum(b for a,b in pairs)
    discord=c[(1,0)]+c[(0,1)]
    k=min(c[(1,0)],c[(0,1)])
    p=min(1.0,2*sum(math.comb(discord,j) for j in range(k+1))/2**discord) if discord else 1.0
    rng=random.Random(42)
    changes=[b-a for a,b in pairs]
    boot=sorted(sum(changes[rng.randrange(200)] for _ in range(200))/200 for _ in range(10000))
    ci=(percentile(boot,.025),percentile(boot,.975))
    if (A,B,c[(1,1)],c[(1,0)],c[(0,1)],c[(0,0)])!=(161,157,153,8,4,35):
        raise AssertionError('Observed counts differ from published findings')
    if not math.isclose(p,0.3876953125,rel_tol=0,abs_tol=1e-13):
        raise AssertionError('McNemar p differs')
    if not all(math.isclose(a,b,rel_tol=0,abs_tol=1e-12) for a,b in zip(ci,(-0.055,0.015))):
        raise AssertionError('Bootstrap interval differs')
    print('RESULT: PASS - derived 200-pair statistics reproduced')
    print(f'ACCURACY: A {A}/200 (80.5%), B {B}/200 (78.5%)')
    print(f'PAIRED: both_correct={c[(1,1)]}, A_only={c[(1,0)]}, B_only={c[(0,1)]}, neither={c[(0,0)]}')
    print(f'EFFECT: {(B-A)/2:.1f} percentage points (B - A)')
    print(f'MCNEMAR_EXACT_TWO_SIDED: {p:.8f}')
    print(f'PAIRED_BOOTSTRAP_95_CI: [{100*ci[0]:.1f}, {100*ci[1]:.1f}] pp')
    print('SCOPE: DERIVED-OUTCOME REPRODUCTION ONLY; NOT RAW-RESPONSE VERIFICATION')


if __name__=='__main__':
    if len(sys.argv)!=2:
        print('Usage: python recompute_paired_statistics.py paired_outcomes_200.csv')
        sys.exit(2)
    try:
        main(Path(sys.argv[1]))
    except Exception as exc:
        print(f'RESULT: FAIL: {type(exc).__name__}: {exc}')
        sys.exit(1)
