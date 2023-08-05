# функция возращает True если число простое, и False если число составное
from math import sqrt


class Prime:
    def __init__(self):
        self.i = 2

    def check(self, n):

        self.limit = int(sqrt(n))

        if n < 2:
            return False
        elif n == 2:
            return True
        
        while self.i <= self.limit:
            if n % self.i == 0:
                return False
            self.i += 1

        return True


