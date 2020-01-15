import logging

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, p: int):
        self.p = p
        self.g = None

    def set_g(self, g):
        """basic: Receives the parameter from the TTP"""
        self.g = g

    def set_sk(self, sk):
        """basic: Receives the key from the TTP"""
        self.sk = sk

    def set_rho(self, rho: int):
        """intuition: sets the 0-share"""
        self.rho = rho
