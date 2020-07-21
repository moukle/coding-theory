from collections import deque
import numpy as np

from . import Code

from galious_field import GF
from polynomial    import Polynomial


class RS(Code):
    def __init__(self, d, q, a=None):
        # TODO: check if q = prime OR factorize in p^d
        self.gf = GF(p=q)

        # set primitive element
        if a: self.a = a
        else: self.a = self.gf.primitive_element()

        Code.__init__(self, n=q-1, k=q-d, q=q, d=d)

    def generator_polynom(self, printing=False):
        # step 1
        polynoms = []
        for i in range(1, self.d):
            ai  = self.a**i
            ai  = self.gf.mod(-ai) # step 2
            aip = Polynomial([ai, 1])
            polynoms.append(aip)

        # step 3
        acc = Polynomial([1])
        for poly in polynoms:
            acc = acc * poly

        # step 4
        g = self.gf.mod(acc)

        if printing:
            print('Generator Polynom:')
            for p in polynoms: print(f'({p})', end="")
            print(f'\n= {acc} mod {self.q}')
            print(f'≅ {g}')
            print(f'-- {g.coeffs}\n')
        return g


    def control_polynom(self, printing=False):
        # step 1
        polynoms = [Polynomial([-self.a**0, 1])]
        for i in range(self.d, self.q-1):
            ai  = self.a**i
            ai  = self.gf.mod(ai) # step 2
            aip = Polynomial([-ai, 1])
            polynoms.append(aip)

        # step 3
        acc = Polynomial([1])
        for poly in polynoms:
            acc = acc * poly

        # step 4
        h = self.gf.mod(acc)

        if printing:
            print('Control Polynom:')
            for p in polynoms: print(f'({p})', end="")
            print(f'\n= {acc} mod {self.q}')
            print(f'≅ {h}')
            print(f'-- {np.flip(h.coeffs)}\n')
        return h


    def generator_matrix(self):
        p = self.generator_polynom()

        padded_coeffs = np.zeros(self.n, dtype=int)
        padded_coeffs[:len(p.coeffs)] = p.coeffs

        coeffs = deque(padded_coeffs)

        G = []
        for _ in range(self.k):
            G.append(list(coeffs))
            coeffs.rotate()

        return np.array(G)


    def control_matrix(self):
        p = self.control_polynom()

        padded_coeffs = np.zeros(self.n, dtype=int)
        padded_coeffs[:len(p.coeffs)] = np.flip(p.coeffs) # care flip (following example 187)

        coeffs = deque(padded_coeffs)

        H = []
        for _ in range(self.n - self.k):
            H.append(list(coeffs))
            coeffs.rotate()

        return np.array(H)


    def vandermonde_matrix(self):
        V = []
        for i in range(1, self.d):
            row = []
            for j in range(self.q - 1):
                row.append(self.gf.mod(self.a**(i*j)))
            V.append(row)

        return np.array(V)
