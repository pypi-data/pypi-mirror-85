from pywork.modules.sort_to_high import Sth

class Bs:

    def __init__ (self):
        pass

    def search(self, arr, item):
        low = 0
        high = len(arr) - 1
        list = Sth().sort(arr)

        while low <= high:
            mid = (low + high)
            guess = list[mid]

            if guess == item:
                return mid
            if guess > item:
                high = mid - 1
            else:
                low = mid + 1 

        return None