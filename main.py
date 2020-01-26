import logging

from poc.aggregator import Aggregator
from poc.participant import Participant
from poc.ttp import TTPBasic
import matplotlib.pyplot as plt
big_delta = 2000  # delta
eps = 0.5
small_delta = 0.001
n = 120
gamma = 0.5

logger = logging.getLogger(__name__)


def experiment_basic(n, t, eps, small_delta, big_delta, gamma):
    """Simulate an aggregation of n participants at time t."""
    # We create the different parties of the experiment
    aggregator = Aggregator()
    participants = [Participant(big_delta) for _ in range(n)]

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
        p.small_delta = small_delta
        p.eps = eps
        p.gamma = gamma
        p.n = n

        p.g, p.P, p.p = ttp.g, ttp.P, ttp.p
        p.sk = ttp.generate_sk()
        p.init_cipher_basic()

    # Now the participants share their private value x to the aggregator
    for p in participants:
        aggregator.append_contribution(p.noisy_enc(t))

    # Once all participants have sent their contribution, the aggretator
    # ... aggregates
    res = aggregator.aggregate_basic(t)
    logger.info("modulo for the experiment: %d" % (ttp.p))
    logger.info("result of the aggregation: %d." % (res))

    real_res = 0
    for p in participants:
        real_res += p.x
    real_res %= ttp.p
    logger.info("real sum: %d." % (real_res))
    logger.info("error: %d" % (modular_abs(res, real_res, ttp.p)))

    return(res, real_res, ttp.p)


def modular_abs(x, y, p):
    return(min((x-y) % p, (y-x) % p))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # L = []
    # for i in range(1000):
    #     res, real_res, p = experiment_basic(n, 1337, eps, small_delta,
    #                                         big_delta, gamma)
    #     L.append((abs(res-real_res)/real_res)*100)
    # plt.hist(L, bins=10)
    # plt.show()
    res, real_res, p = experiment_basic(n, 1337, eps, small_delta,
                                        big_delta, gamma)
