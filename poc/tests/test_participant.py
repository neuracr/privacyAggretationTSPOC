import unittest
from unittest import TestCase
from math import exp

from ..participant import Participant


class Test_Participant(TestCase):

    def test_geom(self):
        big_delta = 2000
        eps = 500
        small_delta = 0.4
        n = 20
        gamma = 1/n
        p = Participant(n)
        p.big_delta = big_delta
        p.small_delta = small_delta
        p.eps = eps
        p.n = n
        p.gamma = gamma

        alpha = exp(eps/big_delta)
        self.assertEqual(p.geom(alpha), 60)


if __name__ == '__main__':
    unittest.main()
