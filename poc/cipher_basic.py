from typing import List
import hashlib
import math


class CipherBasic:
    """Defines the crypto operations explained in section 5.1"""
    def __init__(self, p: int, g: int, sk: int):
        """Initialize the instance for cipher operations.

        Args:
            p: modulo prime for Zp
            g: public parameter
            sk: secret key for R derivation
        """
        self.p = p
        self.g = g
        self.sk = sk

    def _gen_h(self, t: int):
        """Generates the hash for R derivation.
        Args:
            t: time slot id
        """
        return(int(hashlib.sha224(str(t).encode()).hexdigest(), 16) % self.p)

    def noisy_enc(self, x, r, t: int):
        """Encrypt the noised value using the derived key.
        Args:
            x: real value of the participant
            r: noise to add to the value for privacy preservation
            t: time slot id
        """
        H = self._gen_h(t)
        if self.sk < 0:
            H = self.modinv(H, self.p)
        return((
                pow(self.g, (x+r), self.p) * pow(H, abs(self.sk), self.p)
                ) % self.p)

    def aggrDec(self, c: List[int], t: int):
        """The decryption algorithm for the aggregator.
        Args:
            c: list of ciphertexts (noisy encrypted)
            t: time slot id
        """
        H = self._gen_h(t)
        prod = 1
        for ci in c:
            prod = (prod * ci) % self.p
        V = (pow(H, self.sk, self.p) * prod) % self.p
        return(self._discrete_log(V))

    def randomize(self, x: int, r: int):
        """Khi function. Incorporate additive noise for encrypting the data."""
        return (x + r) % self.p

    def _discrete_log(self, x: int):
        """Computes the discrete logarithm of x base g mod p.
        adapted from https://www.geeksforgeeks.org/discrete-logarithm-find
        -integer-k-ak-congruent-modulo-b/"""
        n = int(math.sqrt(self.p) + 1)

        gn = pow(self.g, n, self.p)
        value = [0] * self.p

        cur = gn
        for i in range(1, n + 1):
            if (value[cur] == 0):
                value[cur] = i
            cur = (cur * gn) % self.p

        cur = x
        for i in range(n + 1):
            # Calculate (x ^ j) * g and check for collision
            if (value[cur] > 0):
                ans = value[cur] * n - i
                if (ans < self.p):
                    return(ans)
            cur = (cur * self.g) % self.p
        return(-1)

    # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m
