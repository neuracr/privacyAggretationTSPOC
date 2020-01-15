import unittest
from unittest import TestCase
from ..ttp import TTP


class Test_ttp(TestCase):
    def setUp(self):
        DATA_MAX_BOUND = 2000  # delta
        N = 20  # number of participants
        P = 32323  # P as in Zp (prime number)

        self.ttp = TTP(N, P)

    def test_generate_rho_is_int(self):
        self.assertIsInstance(self.ttp.generate_rho(), int)

    def test_generate_rho_sum_zero(self):
        # initialize the share generator
        self.ttp.init_generator()
        zum = 0

        # generates n+1 shares of 0
        for _ in range(self.ttp.n + 1):
            zum += self.ttp.generate_rho()
        self.assertEqual(zum % self.ttp.p, 0)


if __name__ == '__main__':
    unittest.main()
