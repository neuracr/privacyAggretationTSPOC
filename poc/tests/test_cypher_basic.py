import unittest
import random
from unittest import TestCase

from ..cipher_basic import CipherBasic


class Test_CipherBasic(TestCase):
    def setUp(self):
        self.G = 945  # random generator
        self.P = 32323  # P as in Zp (prime number)
        self.Sk = 685
        self.zero_sum_list = [5745]  # , 21, 4546, 5421, 781, 20012]
        self.zero_sum_list.append((0 - sum(self.zero_sum_list)))
        self.cipher = CipherBasic(self.P, self.G, self.Sk)
    # TODO

    def test__gen_h(self):
        t = 569
        self.assertEqual(sum(self.zero_sum_list), 0)
        H = self.cipher._gen_h(t)
        invH = self.cipher.modinv(H, self.P)

        prod = 1
        for sk in self.zero_sum_list:
            tH = H
            if sk < 0:
                tH = invH
            prod = prod * pow(tH, abs(sk), self.P)
        prod %= self.P
        self.assertEqual(prod, 1)

    def test_discrete_log(self):
        k = random.randint(1, 1000)
        b = pow(self.G, k, self.P)
        self.assertEqual(self.cipher._discrete_log(b), k)


if __name__ == '__main__':
    unittest.main()
