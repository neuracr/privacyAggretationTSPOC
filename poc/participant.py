import logging
from math import exp, log
import random

from .cipher_basic import CipherBasic

logger = logging.getLogger(__name__)


class ParticipantError(Exception):
    pass


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
        self.big_delta = max
        self.sk = None
        self.cipher = None
        self.eps = None
        self.small_delta = None
        self.n = None
        self.gamma = None

    def init_cipher_basic(self):
        self.cipher = CipherBasic(self.p, self.P, self.g, self.sk)

    def noisy_enc(self, t: int):
        r = self.pick_noise()
        logger.debug("noise: %d" % (r))
        return self.cipher.noisy_enc(self.x, r, t)

    def geom(self, alpha):
        """generates a random number that follows the symetric geometric
        probablitity
        """
        def g(k):
            return (alpha-1)/(alpha+1)*alpha**(-abs(k))

        r = random.random()
        s = 0
        i = 0
        while s < r:
            s += g(i)
            if s > r:
                return i
            s += g(-i)
            if s > r:
                return -i
            i += 1

    def pick_noise(self):
        if (not self.big_delta or not self.small_delta or not self.eps or
                not self.n or not self.gamma):
            raise ParticipantError
        alpha = exp(self.eps/self.big_delta)
        beta = 1/(self.gamma*self.n) * log(1/self.small_delta)
        logger.debug("alpha: " + str(alpha) + " beta:" + str(beta))
        ran = random.random()
        logger.debug("random number: " + str(ran))
        if ran < beta:
            return self.geom(alpha)
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
