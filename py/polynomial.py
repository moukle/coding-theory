import numpy as np
from itertools import zip_longest

class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = list(coeffs)

        # prune trailing zeros
        while len(self.coeffs) and self.coeffs[-1] == 0:
            self.coeffs.pop()

    def __bool__(self):
        return self.coeffs != []

    def __add__(self, other):
        coeffs = [a+b for a,b in zip_longest(self.coeffs, other.coeffs, fillvalue=0)]
        return self.__class__(coeffs)

    def __mul__(self, other):
        # other is polynomial
        if type(other) == type(self):
            if self.coeffs and other.coeffs:
                coeffs = np.convolve(self.coeffs, other.coeffs)
                return self.__class__(coeffs)

        # other is scalar
        elif type(other) == int:
            coeffs = [c*other for c in self.coeffs]
            return self.__class__(coeffs)

        return self.__class__([0])

    def deg(self):
        return len(self.coeffs)

    def __str__(self):
        """ return string formatted as aX^3 + bX^2 + c^X + d """

        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        res = []
        for po, co in enumerate(self.coeffs):
            if co:
                if po==0:
                    po = ''
                elif po==1:
                    po = 'x'
                else:
                    po = 'x'+str(po).translate(SUP)
                if co == 1 and po: co = ''
                res.append(str(co)+po)
        if res:
            res.reverse()
            return ' + '.join(res)
        else:
            return "0"

    def __repr__(self):
        return self.__str__()
