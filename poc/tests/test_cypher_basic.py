import unittest
import random
from unittest import TestCase

from ..cipher_basic import CipherBasic
from ..ttp import TTPBasic


class Test_CipherBasic(TestCase):
    def setUp(self):
        ttp = TTPBasic()
        self.p = ttp.p
        self.g = ttp.g
        self.P = ttp.P

    # def test__gen_h(self):
    #     t = 569
    #     cipher = CipherBasic(self.p, self.g, 0)
    #     H = cipher._gen_h(t)
    #     invH = cipher.modinv(H, self.p)

    #     prod = 1
    #     for sk in self.zero_sum_list:
    #         tH = H
    #         if sk < 0:
    #             tH = invH
    #         prod = prod * pow(tH, abs(sk), self.P)
    #     prod %= self.P
        # self.assertEqual(prod, 1)

    # def test_discrete_log(self):
    #     cipher = CipherBasic(self.p, self.g, 0)
    #     k = random.randint(1, 1000)
    #     b = pow(self.g, k, self.p)
    #     self.assertEqual(cipher._discrete_log(b), k)

    def test_noisy_enc_no_noise(self):
        # don't add noise
        for _ in range(5000):
            sk0 = random.randint(0, self.p)
            sk1 = self.p - sk0
            cipher_enc = CipherBasic(self.p, self.P, self.g, sk1)
            x = random.randint(0, 10000)
            t = random.randint(0, 1000000)

            c = cipher_enc.noisy_enc(x, 0, t)

            cipher_dec = CipherBasic(self.p, self.P, self.g, sk0)
            res = cipher_dec.aggrDec([c], t)
            h, hinv = cipher_dec._gen_h(t)
            self.assertEqual(x, res,
                             "Failed: x=%d; c=%d; g=%d; sk0=%d; sk1=%d; t=%d; "
                             "H=%d; p=%d " % (
                                x, c, self.g,
                                sk0, sk1, t, h, self.p))


if __name__ == '__main__':
    unittest.main()
