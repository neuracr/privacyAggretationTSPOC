import logging
import random

logger = logging.getLogger(__name__)


class TTP:
    """Trusted third party entity that deals the random shares"""

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
