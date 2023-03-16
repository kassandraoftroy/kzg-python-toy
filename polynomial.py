from bls12381 import n
from util import mod_inv

# consider using galois package and replacing `lagrange_polynomial`
# with commented alternate implementation below for faster polynomial interpolation
# but much longer wait on startup to load GF(n) and all lookup tables

# from galois import GF, lagrange_poly

# print("...please wait a minute to compute lookup tables for GF(n)...")
# default_f=GF(n,1,verify=False)

# # returns polynomial encoded as an array of coefficients in ascending order
# def lagrange_polynomial(points, f=default_f):
# 	p = lagrange_poly(f([point[0] for point in points]),f([point[1] for point in points]))
# 	coeffs = [int(i) for i in p.coefficients(len(points))]
# 	coeffs.reverse()
# 	return coeffs

def lagrange_polynomial(points, prime=n):
	return __interpolate_polynomial([i[0] for i in points], [k[1] for k in points], prime)

def evaluate_polynomial(polynomial, x_value, prime=n):
	result = polynomial[-1]
	for i in range(2, len(polynomial)+1):
		result = result*x_value
		result = result + polynomial[-i]
	return result%prime

def polynomial_division(polynomial, divisor, prime=n):
	polynomial.reverse()
	c1 = polynomial[0]
	remainder = polynomial[1]
	final_polynomial = []
	for i in range(len(polynomial)-1):
		final_polynomial.append(c1)
		c1=((prime-1)*c1*divisor+remainder)%prime
		if i<len(polynomial)-2:
			remainder=polynomial[i+2]
	final_polynomial.reverse()
	return final_polynomial, remainder

# low-level lagrange interpolation reduced mod prime 
def __interpolate_polynomial(x,y,prime):
	M = [[_x**i*(-1)**(i*len(x)) for _x in x] for i in range(len(x))]
	N = [(M+[y]+M)[d:d+len(x)] for d in range(len(x)+1)]
	C = [__determinant(k) for k in N]
	fac=mod_inv(C[0] * (-1)**(len(x)+1), prime)
	C = [i*fac%prime for i in C]
	return C[1:]

def __determinant(m):
    M = [row[:] for row in m]
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0:
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return 0
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
        prev = M[i][i]
    return sign * M[-1][-1] 
