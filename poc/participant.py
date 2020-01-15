import logging


logger = logging.getLogger(__name__)


class Participant:
    def __init__(self, p: int):
        """Creates a participant.

        Args:
            p: prime defining the Zp additive group
        logger.info("hello, I'm a participant")
        """
        self.p = p

    def set_rho(self, rho: int):
        """Set the 0-share"""
        self.rho = rho
