# KZG Python Toy

This repo is intended to be a very simple toy python implementation of the KZG polynomial commitment and proof scheme over the bls12-381 elliptic curve pairing.

More specifically this is an exercise to take the explanations from [here](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html) and make a real-world implementation of a kate proof system for the evalutation of a single point on P(x) as described in the "Kate Proofs" Section (multiproofs is future work I hope to add here!)

## requirements

python 3+

if you want to use alternate more scalable `lagrange_polynomial` method (see comments in `polynomial.py`) that relies on the galois package, then install one external dependency:

```
pip install galois
```

## test

run test with:

```
python test_kzg.py
```

check out the comments in `test_kzg.py` for more details on what the test is doing!

# quick overview

Given some data `d` we encode it as an array of (x,y) points `(i, d_i) for i in {0...k}` where `d_i` are chunks of the data mapped to `GF(n)`, and `n` is the prime order of the bls12-381 curve.

With `k` points `(i, d_i)` we can interpolate polynomial `P(x)` in GF(n) of degree `k-1` that passes through all k points.

The proof scheme also relies on a set of public elliptic curve points generated in a trusted setup where an unknown secret `s` is used to generate elliptic curve points `s^i * G1 for i in {0,1...k}` where `G1` is the generator point of bls12-381, and one additional elliptic curve point `s*G2` where `G2` is the generator point of the pairing curve (twisted bls12-381). After the trusted setup is complete, we have this array of elliptic curve points and no one knows `s`.

Thus, with the entire data `d`, one can interpolate `P(x)` and use the set of trusted setup elliptic curve points `s^i * G1` to produce commitment `C` to the polynomial `P(x)` where `C = P(s) * G1 = sum (a_i * s^i * G1)` (here `a_i` are the coefficients of `P(x)`)

Holders of any point `(x_p, y_p)` where `P(x_p)=y_p` can prove their point lies on `P(x)` without transmitting or revealing `P(x)`

Instead prover only needs:

- commitment `C` (single field element)
- a proof `pi` (single field element) 
- the point `(x_p, y_p)` being proven (two field elements)

The proof is computed by the prover as `pi = Q(s) * G1 = sum(b_i * s^i * G1)` where `Q(x)` can be computed by prover from `Q(x) = P(x) - y_p / (x - x_p)` (polynomial division in `GF(n)`).

Verifier now takes `C`, `pi`, and `(x_p, y_p)` as well as public values from the trusted setup to verify that the point indeed lies on some `P(x)` that `C` is a commitment to.

They verify the equation `Q(x) * (x - x_p) = P(x) - y_p` at secret point `s` by computing `e(pi, s*G2 - x_p*G2) = e(C - y_p*G1, G2)` where `e` is the pairing operation that allows us to "multiply" elliptic curve points to yeild elements in some resultant finite field. If the two field elements from the equation above are equal, then the proof is accepted, since you could only produce a valid proof if you could find `Q(x)` which you can only do if you know `P(x)` and `(x_p, y_p)` is really a point on it.

Thus we have a ZKP where a verifier can verify that a certain point passes through a particular polynomial that the prover knows and commits to, without the prover revealing anyting further about the polynomial.

Note that in the ethereum danksharding context we don't actually utilize the "zero knowledge" property, but simply use the proofs for compression/efficiency
