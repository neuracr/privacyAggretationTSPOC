import unittest
import random
from unittest import TestCase

from ..participant import Participant


class Test_CipherBasic(TestCase):
    def setUp(self):
        self.G = 945  # random generator
        self.P = 32323  # P as in Zp (prime number)
        self.Sk = 685
        self.DATA_MAX_BOUND = 2000  # delta

        self.participant = Participant(self.P, self.DATA_MAX_BOUND)

    def test_noisy_enc_no_noise(self):
        # don't add noise
        self.participant.x = 123
        self.participant.g = self.G
        self.participant.sk = 99
        self.participant.pick_noise = lambda: 0
        self.participant.init_cipher_basic()

        c = self.participant.noisy_enc(666)
        self.assertEqual(c, 4656)


if __name__ == '__main__':
    unittest.main()
