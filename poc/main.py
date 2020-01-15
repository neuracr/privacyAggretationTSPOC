import logging

from aggregator import Aggregator
from participant import Participant
from ttp import TTPBasic

DATA_MAX_BOUND = 2000  # delta
P = 32323  # P as in Zp (prime number)


def experiment_basic(n):

    # We create the different parties of the experiment
    aggregator = Aggregator(P)
    participants = [Participant(P) for _ in range(n)]
    ttp = TTPBasic(n, P)

    # initialization
    # The TTP chooses a g, p, and generates the sk for each participant and
    # the aggregator
    ttp.init_generator(n)

    # The TTP distributes the parameter and sk to the participants
    # The aggregator gets sk0
    aggregator.g = ttp.get_g()
    aggregator.sk = ttp.generate_sk()

    # The participants receive the parameter and their key
    for p in participants:
        p.g = ttp.get_g()
        p.sk = ttp.generate_sk()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    experiment_basic(20)
