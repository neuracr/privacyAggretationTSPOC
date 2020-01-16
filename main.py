import logging

from poc.aggregator import Aggregator
from poc.participant import Participant
from poc.ttp import TTPBasic

DATA_MAX_BOUND = 2000  # delta
logger = logging.getLogger(__name__)


def experiment_basic(n, t):
    """Simulate an aggregation of n participants at time t."""
    # We create the different parties of the experiment
    aggregator = Aggregator()
    participants = [Participant(DATA_MAX_BOUND) for _ in range(n)]

    # The TTP chooses a g, p, P
    ttp = TTPBasic()

    # initialization
    # The TTP generates the sk for each participant and
    # the aggregator
    ttp.init_generator(n)

    # The TTP distributes the parameter and sk to the participants
    # The aggregator gets sk0
    aggregator.g, aggregator.P, aggregator.p = ttp.g, ttp.P, ttp.p
    aggregator.sk = ttp.generate_sk()
    aggregator.init_cipher_basic()

    # The participants receive the parameter and their key
    for p in participants:
        p.g, p.P, p.p = ttp.g, ttp.P, ttp.p
        p.sk = ttp.generate_sk()
        p.init_cipher_basic()

    # Now the participants share their private value x to the aggregator
    for p in participants:
        aggregator.append_contribution(p.noisy_enc(t))

    # Once all participants have sent their contribution, the aggretator
    # ... aggregates
    res = aggregator.aggregate_basic(t)
    logger.info("result of the aggregation: %d." % (res))

    real_res = 0
    for p in participants:
        real_res += p.x
    real_res %= ttp.P
    logger.info("real sum: %d." % (real_res))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    experiment_basic(20, 1337)
