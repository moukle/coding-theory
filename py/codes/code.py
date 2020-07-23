import numpy as np
from collections import defaultdict

from galious_field import GF
from utils import all_combos

class Code:
    def __init__(self, n, k, q, d=None):
        self.n = n
        self.k = k
        self.q = q
        self.d = d

        self.gf = self.gf # defined by subclass

        print(
                "\n==================================================\n" +
                f"Created Code: {self} \n" +
                "--------------------------------------------------"
            )

    def __str__(self):
        return f'{self.__class__.__name__}({self.n}, {self.k}, {self.d}; {self.q})'

    def generator_matrix(self):
        pass

    def control_matrix(self):
        pass

    def canonic_matrix(self, M):
        C = M.copy()
        rows, cols = C.shape

        r,c = 0,0
        while r < rows and c < cols:
            v_max = C[r:,c].max()
            i_max = C[r:,c].argmax()
            i_max += r

            if not C[i_max, c]:
                c += 1
            else:
                C[[r, i_max], :] = C[[i_max, r], :] # swap rows
                inv    = self.gf.mult_inverse(v_max)
                C[r,:] = self.gf.mod(C[r,:] * inv) # set pivot element to 1

                zero_those_rows = set(range(rows)) - set([r])
                for i in zero_those_rows:
                    inv = self.gf.mod(-C[i,c])
                    C[i,:] = self.gf.mod(C[i,:] + C[r,:]*inv)

                r += 1
                c += 1
        return C

    def systematic_matix(self, M):
        S = M.copy()
        rows, cols = S.shape
        I = np.eye(rows)

        hist = []

        for r in range(rows):
            if (S[:,r] == I[:,r]).all():
                continue

            for i in range(r,cols):
                if (S[:,i] == I[:,r]).all():
                    S[:, [i, r]] = S[:, [r, i]]
                    hist.append([r,i])
                    break

        return S, hist

    def dual_code(self, C):
        C = self.canonic_matrix(C)
        CS, swaps = self.systematic_matix(C)
        r,c = CS.shape

        # (I | P) --> (-P.T | I)
        I  = np.eye(c-r)
        P  = CS[:,r:]
        nP = self.gf.mod(-P)
        CD = np.append(nP.T, I, axis=1)

        # rebuild initial order
        for i,j in swaps:
            CD[:, [j,i]] = CD[:, [i,j]]

        return CD

    def syndrom_table(self, G, H):
        GHT = self.gf.mod(G.dot(H.T))
        if not (GHT == 0).all():
            print('G is not correctly decoded by H')

        T_all = defaultdict(list)
        for v in all_combos(self.gf.p, self.n):
            syndrome = self.gf.mod(v.dot(H.T))
            T_all[tuple(syndrome)].append(list(v))

        T = {}
        for syndrome, equivalences in T_all.items():
            min_w, min_e = self.n, []
            for e in equivalences:
                w = self.hamming_weight(e)
                if w == min_w:
                    min_e.append(e)
                if w < min_w:
                    min_w = w
                    min_e = [e]
            T[syndrome] = min_e
        return T

    def syndrome_decoding(self, v, H, T):
        v = np.array(v)
        syn = self.gf.mod(v.dot(H.T))
        e = T[tuple(syn)][0]
        c = self.gf.mod(v-e)

        if len(T[tuple(syn)]) > 1:
            print("Warning: no clear errortype [might not match mG=c]")
        return c

    def hamming_weight(self, c):
        return sum(np.array(c) != 0)
