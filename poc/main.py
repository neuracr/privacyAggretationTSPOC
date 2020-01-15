import logging

from aggregator import Aggregator
from participant import Participant

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')

    aggregator = Aggregator()
    participant = Participant()
