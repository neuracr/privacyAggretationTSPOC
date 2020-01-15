class Cypher:
    """Defines the crypto operations"""
    def __init__(self):
        print("f33d me numbers.")

    def setup(self, lamda):
        """ Takes in a security parameter λ, and out-
        puts public parameters param, a private key ski for
        each participant, as well as a aggregator capabil-
        ity sk0 needed for decryption of aggregate statistics
        in each time period. Each participant i obtains the
        private key ski , and the data aggregator obtains the
        capability sk0 .
        """

    def noisy_enc(param, ski, t, x, r):
        """ During time step t, each
        participant calls the NoisyEnc algorithm to en-
        code its data x with noise r. The result is a
        noisy encryption of x randomized with the noise
        r. Without risk of ambiguity, we sometimes write
        NoisyEnc(param, ski , t, x
        b ) where b x
        := χ(x, r) is
        the noisy version of the participant’s data, and χ is
        some underlying randomization function.
        """

    def AggrDec(param, sk0, t, c1:List[int]):
        """The decryption
        algorithm takes in the public parameters param, a
        capability sk0 , and ciphertexts c1 , c2 , . . . , c2 for the
        same time period t. For each i ∈ [n], let ci =
        NoisyEnc(ski, t, x
        bi ), where each x
        b i := χ(xi , ri ).
        Let x := (x1 , . . . , xn) and x
        b := (b
        x1 , . . . , x
        b n ). The
        decryption algorithm outputs f (b
        x) which is a noisy
        version of the targeted statistics f (x).
        """