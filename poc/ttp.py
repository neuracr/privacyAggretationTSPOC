import logging
import random

logger = logging.getLogger(__name__)


class GeneratorException(Exception):
    pass


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
            p: p as in Zp
        """
        self.p = p
        self._g = random.randint(0, p-1)
        self.generator = None

    def _init_generator(self, n):
        """Create a generator for the key generator for n participants."""
        _sum = 0
        for _ in range(n):
            rand = random.randint(0, self.p - 1)
            _sum = (_sum + rand) % self.p
            yield(rand)
        yield(self.p - _sum)

    def init_generator(self, n):
        """Initialize the key generator for n participants."""
        logger.info("Initializing sk generator for %d participants" % (n))
        self.generator = self._init_generator(n)

    def generate_sk(self):
        """generates the n+1 capabilities."""
        if not self.generator:
            raise GeneratorException("You must initialize the generator.")
        try:
            return next(self.generator)
        except StopIteration:
            raise GeneratorException(
                "They generator has produced all the keys. Please reinitialize"
                " it to generate a new share of keys.")

    def get_g(self):
        """getter for the public parameter."""
        return(self._g)
