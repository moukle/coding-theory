from galious_field import GF
from polynomial import Polynomial
from codes import RS, HAM, RM

from numpy import flip

def assignment_a():
    gf = GF(2)
    print(gf)

    ip = Polynomial([1,1,1])
    gf = GF(p=2, d=2, ip=ip)
    print(gf)

    ip = Polynomial([1,0,1,1])
    gf = GF(p=2, d=3, ip=ip)
    print(gf)

    ip = Polynomial([2,1,1])
    gf = GF(p=3, d=2, ip=ip)
    print(gf)

    gf.mult_inverse(3)
    gf.mult_inverse(Polynomial([2, 2]))

    gf = GF(p=5, d=2, ip=Polynomial([2,1,1]))


def assignment_b():
    code = RS(d=5, q=7)

    G    = code.generator_matrix()
    GC   = code.canonic_matrix(G)
    print(f"{G=}")
    print(f"{GC=}")

    GCF = flip(GC)
    GS, swaps = code.systematic_matix(GCF)
    # print(f"{GCF=}")
    # print(f"{GS=}")
    # print(f"{swaps=}")

    H = code.dual_code(GC)
    GHT = code.gf.mod(GC.dot(H.T))
    print(f"{H=}")
    print(f"H is {'valid' if (GHT==0).all() else 'INVALID'}") # (GH.T = {GHT})")

    # T = code.syndrom_table(GC, H)
    # c = code.syndrome_decoding([1,2,3,4,5,6], H, T)
    # print(f"{c=}")

    code = HAM(3, 2)
    H = code.control_matrix()
    G = code.generator_matrix()
    print(f"{H=}")
    print(f"{G=}")
    print(f"{code.gf.mod(G.dot(H.T))=}")

    code = RM(1, 2)
    G = code.generator_matrix()
    H = code.control_matrix()
    print(f"{G=}")
    print(f"{code.gf.mod(G.dot(H.T))=}")



def assignment_c():
    rs = RS(d=5, q=7)
    rs.generator_polynom(printing=True)
    rs.control_polynom(printing=True)

    G = rs.generator_matrix()
    H = rs.control_matrix()

    print(f"{G=}\n")
    print(f"{H=}\n")
    print(f"GH^T = \n{rs.gf.mod(G.dot(H.T))}\n")

    V = rs.vandermonde_matrix()
    print(f"{V=}\n")
    print(f"GV^T = \n{rs.gf.mod(G.dot(V.T))}\n")

    T = rs.syndrom_table(G, H)
    v1 = [4, 2, 3, 6, 1, 1]
    v2 = [4, 2, 3, 6, 2, 1]
    v3 = [4, 2, 3, 7, 2, 1]
    c1 = rs.syndrome_decoding(v1,H, T); print(f"{v1=} -> {c1=}")
    c2 = rs.syndrome_decoding(v2,H, T); print(f"{v2=} -> {c2=}")
    c3 = rs.syndrome_decoding(v3,H, T); print(f"{v3=} -> {c3=}")

if __name__ == "__main__":
    # assignment_a()
    assignment_b()
    # assignment_c()
