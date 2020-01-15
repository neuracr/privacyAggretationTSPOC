import logging

from aggregator import Aggregator
from participant import Participant

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')

    # constants
    DATA_MAX_BOUND = 2000  # delta
    N = 20  # number of participants
    P = 32323  # P as in Zp (prime number)

    aggregator = Aggregator()
    participants = [Participant(P) for _ in range(N)]
