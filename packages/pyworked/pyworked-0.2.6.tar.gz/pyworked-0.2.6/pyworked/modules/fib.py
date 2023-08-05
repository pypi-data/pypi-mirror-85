class Fib:

    def __init__(self):
        self.fib1 = 1
        self.fib2 = 1
        self.i = 0

    def find(self, number):
        while self.i < number - 2:
            fib_sum = self.fib1 + self.fib2
            self.fib1 = self.fib2
            self.fib2 = fib_sum
            self.i = self.i + 1

        return(self.fib2)