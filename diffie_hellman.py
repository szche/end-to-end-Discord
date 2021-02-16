from math import pow
from random import randint

class DiffieHellman(object):
    def __init__(self):
        self.p = 23
        self.g = 5

    def generate_k(self):
        self.x = randint(2, self.p)
        self.k1 = int(pow(self.g, self.x) % self.p)
        return self.k1

    def generate_full_key(self, k2):
        self.k2 = int(k2)
        self.key = int(pow(self.k2, self.x) % self.p)
        return self.key


