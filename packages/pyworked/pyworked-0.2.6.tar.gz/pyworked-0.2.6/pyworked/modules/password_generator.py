import random

class Pass:

    def __init__(self):
        self.chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.password = ''

    def generate(self, length):
        for i in range(length):
            self.password += random.choice(self.chars)
        
        return self.password