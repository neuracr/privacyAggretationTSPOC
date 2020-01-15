import unittest
import random
from unittest import TestCase

from ..cipher_basic import CipherBasic


class Test_CipherBasic(TestCase):
    def setUp(self):
        self.G = 945  # random generator
        self.P = 32323  # P as in Zp (prime number)
        self.Sk = 685

        self.cipher = CipherBasic(self.P, self.G, self.Sk)
    # TODO

    def test_discrete_log(self):
        k = random.randint(1, 1000)
        b = pow(self.G, k, self.P)
        self.assertEqual(self.cipher.discrete_log(b), k)


if __name__ == '__main__':
    unittest.main()
