from math import pow
from random import randint

class DiffieHellman(object):
    def __init__(self, k2):
        self.p = 23
        self.g = 5
        self.k2 = k2

    def generate_k(self):
        self.x = randint(2, self.p)
        self.k1 = int(pow(self.g, self.x) % self.p)
        return self.k1

    def generate_full_key(self):
        self.key = int(pow(self.k2, self.x) % self.p)
        return self.key




if __name__ == "__main__":
    df = DiffieHellman(8)
    df.generate_k()
    print(df.generate_full_key())

