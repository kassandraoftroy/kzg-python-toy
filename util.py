import hashlib
from secrets import randbelow

def hash256(m):
    if type(m) != bytes:
        m = m.encode("utf-8")
    return hashlib.sha256(m).digest()

# modular math
def mod_inv(x, p):
	assert gcd(x, p) == 1, "Divisor %d not coprime to modulus %d" % (x, p)
	z, a = (x % p), 1
	while z != 1:
		q = - (p // z)
		z, a = (p + q * z), (q * a) % p
	return a

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

# cryptographically secure random number generation in a given range
def rand_int(prime):
	return __randrange(1, prime-1)

def __randrange(lower, upper):
	return randbelow(upper-lower)+lower
