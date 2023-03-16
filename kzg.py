from util import rand_int
from bls12381 import n
from ec import G1Generator, G2Generator
from polynomial import lagrange_polynomial, polynomial_division
from binascii import hexlify
from pairing import ate_pairing

G1 = G1Generator()
G2 = G2Generator()

default_length=64

def trusted_setup(length=default_length):
    s = rand_int(n)
    s_powers = [s**i%n for i in range(length)]
    return [j*G1 for j in s_powers], s*G2

def encode_as_polynomial(data, length=default_length):
    chunk_size=31 # max bytes that safely map to prime order group (n)
    data = __format_data(data, length*chunk_size)
    points = [(i,int(hexlify(data[i*chunk_size:(i+1)*chunk_size]).decode(), 16)) for i in range(length)]
    polynomial = lagrange_polynomial(points)
    return points, polynomial

def commit(polynomial, setup_g1):
    assert len(polynomial) == len(setup_g1), "polynomial too large"
    return sum([i1*i2 for i1, i2 in zip(polynomial, setup_g1)])

def proof(polynomial, point, setup_g1):
    assert len(polynomial)-1<=len(setup_g1), "polynomial too large"
    px_minus_y = [((n-1)*point[1]+polynomial[0])%n]+polynomial[1:]
    qx, remainder = polynomial_division(px_minus_y,(n-1)*point[0])
    assert remainder==0, "point not on polynomial"
    return sum([i1*i2 for i1, i2 in zip(qx, setup_g1[:len(qx)])])

def verify(commitment,proof,point,s_g2):
    s_minus_x=(n-point[0])*G2+s_g2
    result=ate_pairing(proof, s_minus_x)
    c_minus_y=(n-point[1])*G1+commitment
    return result==ate_pairing(c_minus_y, G2)

def __format_data(data, data_len):
    if type(data) != bytes:
        data = data.encode("utf-8")
    assert len(data) <= data_len, "data too large"
    if len(data) < data_len:
        padding = b'\x00'*(data_len-len(data))
        data = data + padding
    return data
