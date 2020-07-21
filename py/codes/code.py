import numpy as np
from galious_field import GF

class Code:
    def __init__(self, n, k, q, d=None):
        self.n = n
        self.k = k
        self.q = q
        self.d = d

        self.gf = self.gf # defined by subclass
        print(f"Created Code: {self} \n")

    def __str__(self):
        return f'{self.__class__.__name__}({self.n}, {self.k}, {self.d}; {self.q})'

    def generator_matrix(self):
        pass

    def control_matrix(self):
        pass

    def canonic_matrix(self, M):
        rows, cols = M.shape

        r,c = 0,0
        while r < rows and c < cols:
            v_max = M[r:,c].max()
            i_max = M[r:,c].argmax()
            i_max += r

            if not M[i_max, c]:
                c += 1
            else:
                M[[r, i_max], :] = M[[i_max, r], :] # swap rows
                inv    = self.gf.mult_inverse(v_max)
                M[r,:] = self.gf.mod(M[r,:] * inv)

                zero_those_rows = set(range(rows)) - set([r])
                for i in zero_those_rows:
                    inv = self.gf.mod(-M[i,c])
                    M[i,:] = self.gf.mod(M[i,:] + M[r,:]*inv)

                r += 1
                c += 1
        return M

    def dual_code(self, C):
        pass


# depr: remove after some more testing
    # for i in range(r+1, rows): # fill rows below in pivotcolumn c with zeros
        # inv = self.gf.mod(-M[i,c])
        # M[i,:] = self.gf.mod(M[i,:] + M[r,:]*inv)
    # for i in range(0, r): # fill rows above in pivotcolumn c with zeros
        # inv = self.gf.mod(-M[i,c])
        # M[i,:] = self.gf.mod(M[i,:] + M[r,:]*inv)
