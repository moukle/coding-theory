from galious_field import GF
from polynomial import Polynomial
from codes import RS

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
    print(GC)


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


if __name__ == "__main__":
    # assignment_a()
    assignment_b()
    # assignment_c()
