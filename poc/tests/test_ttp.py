import unittest
from unittest import TestCase
from ..ttp import TTPBasic
# from ..ttp import TTPIntuition


# class Test_ttpIntuition(TestCase):
#     def setUp(self):
#         N = 20  # number of participants

#         self.ttp = TTPIntuition(N, P)

#     def test_generate_rho_is_int(self):
#         self.assertIsInstance(self.ttp.generate_rho(), int)

#     def test_generate_rho_sum_zero(self):
#         # initialize the share generator
#         self.ttp.init_generator()
#         zum = 0

#         # generates n+1 shares of 0
#         for _ in range(self.ttp.n + 1):
#             zum += self.ttp.generate_rho()
#         self.assertEqual(zum % self.ttp.p, 0)


# class Test_ttpBasic(TestCase):
#     def setUp(self):
#         self.N = 20  # number of participants
#         self.lam = 64

#         self.ttp = TTPBasic(self.P, self.lam)

#     def test_generate_sk_is_int(self):
#         self.ttp.init_generator(self.N)
#         self.assertIsInstance(self.ttp.generate_sk(), int)

#     def test_generate_sk_sum_zero(self):
#         # initialize the share generator
#         self.ttp.init_generator(self.N)
#         zum = 0

#         # generates n+1 shares of 0
#         for _ in range(self.N + 1):
#             zum += self.ttp.generate_sk()
#         self.assertEqual(zum % self.ttp.p, 0)
# TODO

if __name__ == '__main__':
    unittest.main()
