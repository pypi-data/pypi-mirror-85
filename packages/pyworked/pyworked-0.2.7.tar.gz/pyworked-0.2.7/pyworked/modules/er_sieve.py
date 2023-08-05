class Es:

    def __init__(self):
        pass

    def search(self, n):
        mask = [1] * (n - 1)
        numbers = list()

        for i in range(2, int(n / 2)):
            t = 2 * i

            while t <= n:
                mask[t - 2] = 0
                t += i
        
        for i in range(len(mask)):
            if mask[i] != 0:
                numbers.append(i + 2)

        return numbers