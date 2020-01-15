from typing import List


class CipherIntuition:
    """Defines the crypto operations explained in section 5.1"""
    def __init__(self, p: int):
        """Initialize the instance for cipher operations.

        Args:
            p: modulo prime for Zp
        """
        self.p = p

    def noisy_enc(self, rho, x, r):
        """Encrypt the noised value using the 0-share.
        Args:
            rho: 0-share specific to the participant
            x: real value of the participant
            r: noise to add to the value for privacy preservation
        """
        return((x + r + rho) % self.p)

    def AggrDec(self, aggregator_rho, c: List[int]):
        """The decryption algorithm for the aggregator.
        Args:
            aggregator_rho: the zero share of the aggregator
            c: list of ciphertexts (noisy encrypted)
        """
        return(aggregator_rho + sum(c))

    def randomize(self, x: int, r: int):
        """Khi function. Incorporate additive noise for encrypting the data."""
        return (x + r) % self.p
