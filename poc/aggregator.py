import logging

from .cipher_basic import CipherBasic

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self):
        self.p = None
        self.g = None
        self.P = None
        self.cipher = None
        self.contributions = []

    def init_cipher_basic(self):
        self.cipher = CipherBasic(self.p, self.P, self.g, self.sk)

    def append_contribution(self, c):
        self.contributions.append(c)

    def aggregate_basic(self, t):
        return self.cipher.aggrDec(self.contributions, t)

    def set_g(self, g):
        """basic: Receives the parameter from the TTP"""
        self.g = g

    def set_sk(self, sk):
        """basic: Receives the key from the TTP"""
        self.sk = sk

    def set_rho(self, rho: int):
        """intuition: sets the 0-share"""
        self.rho = rho
