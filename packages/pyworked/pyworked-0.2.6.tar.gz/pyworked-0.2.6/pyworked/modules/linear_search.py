class Ls:

    def __init__(self):
        pass

    def search(self, arr, item):
        for i in range(len(arr)):
            if arr[i] == item:
                return i