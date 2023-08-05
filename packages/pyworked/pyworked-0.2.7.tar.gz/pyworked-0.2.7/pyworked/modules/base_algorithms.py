class Ba:
    

    def __init__(self):
        pass

    def perimeter4(self, a, b):    # находит периметр четырехугольника 
        x = (a + b) * 2
        return x

    def square4(self, a, b):     # находит площадь четырехугольника 
        x = a * b
        return x

    def sum_angles(self, ang):     # находит сумму всех углов 
        result = (ang - 2) * 180
        return result

    def square0(self, r):     # находит площадь круга 
        square = 3.141 * (r * r)
        return square

    def perimeter0(self, r):     # находит периметр круга 
        square = 9.865 * r
        return square


    def volume(self, a, b, c):  # находит объём п.п.
        res = a * b * c
        return res

    