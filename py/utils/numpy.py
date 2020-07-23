import numpy as np

def all_combos(q, n):
    if n < 1:
        return np.array([[]])

    alphabets = [list(np.arange(q)) for _ in range(n)]
    combos = np.array(np.meshgrid(*alphabets)).T.reshape(-1,n)

    return combos
