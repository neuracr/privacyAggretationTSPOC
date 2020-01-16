import logging
import random

from .cipher_basic import CipherBasic

logger = logging.getLogger(__name__)


class Participant:
    def __init__(self, max: int):
        """Creates a participant.

        The Participant class can work in the "intuition" and in the "basic"
        case.
        Args:
            p: prime defining the Zp additive group
            max: maximum value for the stat
        """
        self.p = None
        self.g = None
        self.P = None
        self.x = random.randint(0, max)
        self.max = max
        self.sk = None
        self.cipher = None

    def init_cipher_basic(self):
        self.cipher = CipherBasic(self.p, self.P, self.g, self.sk)

    def noisy_enc(self, t: int):
        r = self.pick_noise()
        return self.cipher.noisy_enc(self.x, r, t)

    def pick_noise(self):
        # TODO
        return 0

    def set_g(self, g):
        """basic: Receives the parameter from the TTP"""
        self.g = g

    def set_sk(self, sk):
        """basic: Receives the key from the TTP"""
        self.sk = sk

    def set_rho(self, rho: int):
        """intuition: sets the 0-share"""
        self.rho = rho
