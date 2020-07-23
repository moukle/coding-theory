import numpy as np

from . import Code
from galious_field import GF

from utils import all_combos


class HAM(Code):
    def __init__(self, m, q):
        # TODO: check if q = prime OR factorize in p^d
        self.gf = GF(p=q)
        self.m = m

        n = int((q**m-1) / (q-1))
        k = int(n - m)
        d = 3
        Code.__init__(self, n=n, k=k, q=q, d=d)


    def T(self):
        T = []
        for a in range(self.m-1, -1, -1):
            heads = np.zeros((self.q**a, self.m - a), dtype=int)
            heads[:,-1] = 1

            tails = all_combos(self.q, a)

            T.extend([list(h)+list(t) for h,t in zip(heads,tails)])
        return T


    def control_matrix(self):
        return np.array(self.T()).T


    def generator_matrix(self):
        return self.dual_code(self.control_matrix())
