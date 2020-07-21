class Code:
    def __init__(self, n, k, q, d=None):
        self.n = n
        self.k = k
        self.q = q
        self.d = d

        print(f"Created Code: {self} \n")

    def __str__(self):
        return f'{self.__class__.__name__}({self.n}, {self.k}, {self.d}; {self.q})'

    def generator_matrix(self):
        pass

    def control_matrix(self):
        pass
