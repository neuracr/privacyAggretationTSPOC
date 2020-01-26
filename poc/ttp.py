import logging
import random


logger = logging.getLogger(__name__)
# https://github.com/cryptosense/diffie-hellman-groups/tree/master/gen
dh_settings = [{
    "g": 2,
    "length": 512,
    "name": "OpenSSL 512-bit",
    "p": 11435638110073884015312138951374632602058080675070521707579703088370446597672067452229024566834732449017970455481029703480957707976441965258194321262569523,
    "prime": True,
    "safe_prime": True
}, {
    "p": 955103,
}]


class GeneratorException(Exception):
    pass


# class TTPIntuition:
#     """Trusted third party entity that deals the random shares as in 5.1"""

#     def __init__(self, n: int, p: int):
#         """
#         Args:
#             n: number of participants
#             p: p as in Zp
#         """
#         self.n = n
#         self.p = p
#         self.generator = None

#     def init_generator(self):
#         logger.info("creating new zero-shares")
#         _sum = 0
#         for _ in range(self.n):
#             rand = random.randint(0, self.p - 1)
#             _sum = (_sum + rand) % self.p
#             yield(rand)
#         yield(self.p - _sum)

#     def generate_rho(self):
#         if not self.generator:
#             self.generator = self.init_generator()
#         try:
#             return next(self.generator)
#         except StopIteration:
#             self.generator = self.init_generator()
#             return next(self.generator)


class TTPBasic:
    """Trusted third party entity that deals public param g and sk as in 5.2"""

    def __init__(self, P: int = dh_settings[1]["p"], l: int = 1024):
        """
        Args:
            P: safe_prime to generate the group (not the p of Zp)
            l: lambda security parameter
        """
        self.p, self.g = generate_group(P)
        self.P = P
        self.sk_generator = None

        # security parameter for the sk
        self.lam = l
        logger.debug("p:%d P:%d g:%d" % (self.p, self.P, self.g))
    # def pick_g(self):
    #     """Picks a generator of Zp*"""
    #     g = random.randint(0, self.p-1)
    #     while(gcd(g, self.p-1) != 1):
    #         g = random.randint(0, self.p-1)
    #     return g

    def _init_generator(self, n):
        """Create a generator for the key generator for n participants."""
        _sum = 0
        for _ in range(n):
            rand = random.randint(0, self.p-1)
            _sum = (_sum + rand) % self.p
            yield(rand)
        yield(self.p - _sum)

    def init_generator(self, n):
        """Initialize the key generator for n participants."""
        logger.info("Initializing sk generator for %d participants" % (n))
        self.sk_generator = self._init_generator(n)

    def generate_sk(self):
        """generates the n+1 capabilities."""
        if not self.sk_generator:
            raise GeneratorException("You must initialize the generator.")
        try:
            return next(self.sk_generator)
        except StopIteration:
            raise GeneratorException(
                "They generator has produced all the keys. Please reinitialize"
                " it to generate a new share of keys.")


def generate_group(P):
    """generates a group from safe prime P.
    Returns:
        q: the order of the group (prime)
        g: a generator
    """
    # http://u.cs.biu.ac.il/~lindell/89-656/group%20example.pdf

    # we assume p is a safe prime (p = 2q+1 and q is prime)
    q = int((P-1)/2)
    g = int(pow(random.randint(2, 1000), 2, P))
    return(q, g)
