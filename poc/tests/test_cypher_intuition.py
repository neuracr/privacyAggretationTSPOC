import unittest
from unittest import TestCase
from ..cipher_intuition import CipherIntuition


class Test_CipherIntuition(TestCase):
    def setUp(self):
        DATA_MAX_BOUND = 2000  # delta
        N = 20  # number of participants
        P = 32323  # P as in Zp (prime number)

        self.cipher = CipherIntuition(P)

    # TODO


if __name__ == '__main__':
    unittest.main()
