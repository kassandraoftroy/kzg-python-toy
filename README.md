# KZG Python Toy

This repo is intended to be a very simple and readable toy implementation of the actual KZG commitment and proof scheme over the bls12-381 elliptic curve pairing in python.

More specifically this takes the explanations from [here](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html) and tries to make a real world implementation of the "single" kate proof (multiproofs is future work I hope to add here!)

# quick overview

Data is chunked into i={0...n} chunks d_i and represented as points (i, d_i) or as the lagrange interpolating polynomial P(x) that passes through all these points in GF(n) where n is the order of the bls12-381 curve.

holders of any point (i, y_i) where P(i)=y_i can prove their point lies on P(x) without transmitting or revealing P(x)

Instead prover only transmits:

- commitment to P(x) C (single field element)
- a proof pi (single field element) 
- the point (i, y_i) being proven (two field elements)

Verifier can take C, pi, and (i, y_i) as well as public values from the trusted setup to verify that the point indeed lies on P(x).

Thus we have a ZKP where a verifier can verify that a certain point passes through a particular polynomial of a given degree that the prover knows, without the prover revealing anyting further about the polynomial.

In the ethereum danksharding context we don't actually utilize the "zero knowledge" property but simply use the proofs for compression/efficiency (the secrecy of the polynomial is not a requirement)
