#
# Elliptic Curve Equation
#
# y^2 = x^3 + a*x + b (mod p)
#


class CurveFp:

    def __init__(self, A, B, P, N, Gx, Gy, name):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.Gx = Gx
        self.Gy = Gy
        self.name = name

    def contains(self, x,y):
      """Is the point R(x,y) on this curve?"""
      return (y**2 - (x**3 + self.A * x + self.B)) % self.P == 0

    # Tonelli–Shanks, this algorithm can work
    def x2y(self,x, odev):
        a = (x**3 + self.A * x + self.B)% self.P
        y1, y2 = self.mod_sqrt(a, self.P)
        if y1%2 == odev:
            return y1
        else:
            return y2

    def length(self):
        return (1 + len("%x" % self.N)) // 2

    # copy from util.py in fastecdsa
    def _tonelli_shanks(self, n, p):
        '''A generic algorithm for computng modular square roots.'''
        Q, S = p - 1, 0
        while Q % 2 == 0:
            Q, S = Q // 2, S + 1

        z = 2
        while pow(z, (p - 1) // 2, p) != (-1 % p):
            z += 1

        M, c, t, R = S, pow(z, Q, p), pow(n, Q, p), pow(n, (Q + 1) // 2, p)
        while t != 1:
            for i in range(1, M):
                if pow(t, 2**i, p) == 1:
                    break

            b = pow(c, 2**(M - i - 1), p)
            M, c, t, R = i, pow(b, 2, p), (t * b * b) % p, (R * b) % p

        return R, -R % p
    # copy from util.py in fastecdsa
    def mod_sqrt(self, a, p):
        '''Compute the square root of :math:`a \pmod{p}`
        In other words, find a value :math:`x` such that :math:`x^2 \equiv a \pmod{p}`.
        Args:
            |  a (long): The value whose root to take.
            |  p (long): The prime whose field to perform the square root in.
        Returns:
            (long, long): the two values of :math:`x` satisfying :math:`x^2 \equiv a \pmod{p}`.
        '''
        if p % 4 == 3:
            k = (p - 3) // 4
            x = pow(a, k + 1, p)
            return x, (-x % p)
        else:
            return self._tonelli_shanks(a, p)


secp256k1 = CurveFp(
    name="secp256k1",
    A=0x0000000000000000000000000000000000000000000000000000000000000000,
    B=0x0000000000000000000000000000000000000000000000000000000000000007,
    P=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    N=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    Gx=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    Gy=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)

supportedCurves = [
    secp256k1
]

curvesByOid = {
    (1, 3, 132, 0, 10): secp256k1
}