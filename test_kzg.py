import kzg
from polynomial import evaluate_polynomial

if __name__=='__main__':
    print("run kzg proof test:")
    # run trusted setup and store public setup points
    setup_g1, s_g2 = kzg.trusted_setup()

    # encode data as polynomial P(x)
    data=b'\xff'*1000 # random data
    points, poly = kzg.encode_as_polynomial(data)

    # create kzg commitment to P(x)
    C = kzg.commit(poly, setup_g1)

    # choose some point on P(x) to prove
    point = (1, evaluate_polynomial(poly,1))
    assert points[1][0] == point[0], "xs should be equal"
    assert points[1][1] == point[1], "ys should be equal"

    # create kzg proof
    pi = kzg.proof(poly, point, setup_g1)

    # verifier can verify proof that point is on P(x)
    # with only commitment C, proof pi, and point
    assert kzg.verify(C,pi,point,s_g2), "test fail: valid proof rejected"

    # proof fails if pass wrong point
    wrong_point=(point[1], point[0])
    assert not kzg.verify(C,pi,wrong_point,s_g2), "test fail: uncaught invalid proof"
    
    print("SUCCESS!")