class Nod:

    def __init__(self):
        pass

    def search(self, a, b):
        while (a != 0) and (b != 0):
            if a < b:
                a, b = b, a
            a %= b

        return a + b
