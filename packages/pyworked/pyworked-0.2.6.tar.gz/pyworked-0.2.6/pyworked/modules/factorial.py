class Factorial:
    
    def __init__(self):
        self.factorial = 1

    def find(self, number):
        for i in range(2, number + 1):
            self.factorial *= i

        return(self.factorial)
        