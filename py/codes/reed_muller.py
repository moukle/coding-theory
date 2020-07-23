import numpy as np
from scipy.special import binom

from . import Code
from galious_field import GF

from utils import all_combos


class RM(Code):
    def __init__(self, r, m):
        n = 2**m
        k = int(np.sum([binom(m, i) for i in range(r+1)]))
        d = 2**(m-r)
        q = 2

        self.r = r
        self.m = m
        self.gf = GF(p=q)

        Code.__init__(self, n=n, k=k, q=q, d=d)


    def G(self, r, m):
        if r == 0:
            return np.ones((2**m), dtype=int)
        elif r <= m:
            G0 = self.G(r, m-1)
            G3 = self.G(r-1, m-1)
            G2 = np.zeros(G3.shape, dtype=int)

            r0 = np.hstack(([G0, G0]))
            r1 = np.hstack(([G2, G3]))
            return np.vstack((r0, r1))
        else:
            return self.G(m, m)


    def generator_matrix(self):
        return self.G(self.r, self.m)


    def control_matrix(self):
        return self.dual_code(self.generator_matrix())
