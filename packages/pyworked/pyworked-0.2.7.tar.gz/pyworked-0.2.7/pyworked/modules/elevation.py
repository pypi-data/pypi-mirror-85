class El:

    def __init__(self):
        pass

    def elevate(self, number, elev):
        if elev == 0:
            return(1)
        if elev % 2 == 0:
            return(self.elevate(number * number, elev // 2))
        else:
            return(number * self.elevate(number, elev - 1))
