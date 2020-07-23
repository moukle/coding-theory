import random; random.seed(42)
import numpy as np

import pandas as pd
from tabulate import tabulate

from polynomial import Polynomial
from utils import is_permutation, all_combos

class GF:
    def __init__(self, p, d=1, ip=None):
        self.p = p
        self.d = d
        self.q = p ** d
        self.ip = ip


    def __str__(self):
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        d_sup = str(self.d).translate(SUP)
        return f"================================================== \
                GF({self.p}{d_sup}{', '+str(self.ip) if self.ip else ''}) \
                \n + \n{self.addition_table()} \
                \n * \n{self.multiplication_table()}\n\n"


    def addition_table(self):
        combos = all_combos(self.p, self.d)
        combos = [Polynomial(c) for c in combos]
        A_df = pd.DataFrame(columns=combos)

        for p1 in combos:
            row = []
            for p2 in combos:
                row.append(self.mod(p1 + p2))
            A_df.loc[p1] = row
        return tabulate(A_df, headers='keys', tablefmt='psql')


    def multiplication_table(self):
        combos = all_combos(self.p, self.d)
        combos = [Polynomial(c) for c in combos]
        M_df = pd.DataFrame(columns=combos)

        for p1 in combos:
            row = []
            for p2 in combos:
                row.append(self.mod(p1 * p2))
            M_df.loc[p1] = row
        return tabulate(M_df, headers='keys', tablefmt='psql')


    def mod(self, e):
        if type(e) == Polynomial:
            if self.ip:
                e = self.mod_ip(e)
            return Polynomial([self.mod(c) for c in e.coeffs])
        else:
            return e % self.p


    def mod_ip(self, e):
        while e.deg() >= self.ip.deg():
            cf = [0] * (e.deg() - self.ip.deg() + 1)
            cf[-1] = -e.coeffs[-1]
            cf = Polynomial(cf) * self.ip

            e += cf
            e = self.mod(e)
        return e


    def mult_inverse(self, e, printing=False) -> int:
        inv = -1
        e = self.mod(e)

        if not e:
            if printing:
                print(f"`{e}*` got no multiplicative inverse")
            return inv

        # a^q-1=1, thus a^-1=a^q-2
        if type(e) == int or type(e) == np.int64:
            inv = e ** (self.q - 2)

        if type(e) == Polynomial:
            inv = Polynomial([1])
            for _ in range(self.q - 2):
                inv *= e

        if inv != -1:
            inv = self.mod(inv)

        if printing:
            print(f"{e=} * {inv=} is {self.mod(e*inv)} ({type(e)=})")

        return inv


    def primitive_element(self) -> int:
        all_elems_star = [i for i in range(1, self.q)]

        for elem in all_elems_star:
            a = [self.mod(elem**i) for i in range(self.q-1)]
            if is_permutation(a, all_elems_star):
                return elem


    # zzzz - NO
    """
    def div(self, a, b):
        quotient = Polynomial([0])
        while a.deg() >= b.deg():
            cf = [0] * (a.deg() - b.deg() + 1)
            cf[-1] = a.coeffs[-1]
            cf = Polynomial(cf) * b

            quotient += cf

            a += cf
            a = Polynomial([self.mod(c) for c in a.coeffs])
        quotient = Polynomial([self.mod(c) for c in quotient.coeffs])
        return quotient, a


    def egcd(self, a, b):
        if a.coeffs == []:
            return (b, Polynomial([0]), Polynomial([1]))
        else:
            gcd, x, y = self.egcd(self.div(b, a)[1], a)
            return (gcd, y + self.div(b,a)[0] * x, x)
    """
