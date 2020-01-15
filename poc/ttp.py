import logging
import random

logger = logging.getLogger(__name__)


class TTPIntuition:
    """Trusted third party entity that deals the random shares as in 5.1"""

    def __init__(self, n: int, p: int):
        """
        Args:
            n: number of participants
            p: p as in Zp
        """
        self.n = n
        self.p = p
        self.generator = None

    def init_generator(self):
        logger.info("creating new zero-shares")
        _sum = 0
        for _ in range(self.n):
            rand = random.randint(0, self.p - 1)
            _sum = (_sum + rand) % self.p
            yield(rand)
        yield(self.p - _sum)

    def generate_rho(self):
        if not self.generator:
            self.generator = self.init_generator()
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = self.init_generator()
            return next(self.generator)


class TTPBasic:
    """Trusted third party entity that deals public param g and sk as in 5.2"""

    def __init__(self, n: int, p: int):
        """
        Args:
            n: number of participants
            p: p as in Zp
        """
        self.n = n
        self.p = p
        self._g = random.randint(0, p-1)
        self.generator = None

    def init_generator(self):
        logger.info("initializing sks generator")
        _sum = 0
        for _ in range(self.n):
            rand = random.randint(0, self.p - 1)
            _sum = (_sum + rand) % self.p
            yield(rand)
        yield(self.p - _sum)

    def generate_sk(self):
        """generates the n+1 capabilities."""
        if not self.generator:
            self.generator = self.init_generator()
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = self.init_generator()
            return next(self.generator)

    def get_g(self):
        """getter for the public parameter."""
        return(self._g)
