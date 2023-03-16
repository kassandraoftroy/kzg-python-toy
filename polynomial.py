from bls12381 import n
from galois import GF, lagrange_poly

print("...please wait a minute to compute lookup tables for GF(n)...")
default_f=GF(n,1,verify=False)

# returns polynomial encoded as an array of coefficients in ascending order
def lagrange_polynomial(points, f=default_f):
	p = lagrange_poly(f([point[0] for point in points]),f([point[1] for point in points]))
	coeffs = [int(i) for i in p.coefficients(len(points))]
	coeffs.reverse()
	return coeffs

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

# def lagrange_polynomial(points, prime=n):
# 	return __interpolate_polynomial([i[0] for i in points], [k[1] for k in points], prime)

# def __interpolate_polynomial(x,y,prime):
# 	M = [[_x**i*(-1)**(i*len(x)) for _x in x] for i in range(len(x))]
# 	N = [(M+[y]+M)[d:d+len(x)] for d in range(len(x)+1)]
# 	C = [__determinant(k, prime) for k in N]
# 	fac=mod_inv(C[0] * (-1)**(len(x)+1), prime)
# 	C = [i*fac%prime for i in C][1:]
# 	return C[1:]

# def __determinant(m, prime):
# 	return getMatrixDeterminant(m, prime)

# def getMatrixMinor(m,i,j):
#     return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# def getMatrixDeterminant(m, prime):
#     #base case for 2x2 matrix
#     if len(m) == 2:
#         return (m[0][0]*m[1][1]+m[0][1]*m[1][0]*(prime-1))%prime

#     determinant = 0
#     for c in range(len(m)):
#         determinant += ((-1)**c)*m[0][c]*getMatrixDeterminant(getMatrixMinor(m,0,c), prime)
#     return determinant%prime
