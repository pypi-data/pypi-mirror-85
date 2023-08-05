class Sth:

    def __init__(self):
        pass

    def find(self, arr):
        smallest = arr[0]
        smallest_index = 0

        for i in range(1, len(arr)):
            if arr[i] < smallest:
                smallest = arr[i]
                smallest_index = i
    
        return smallest_index

    def sort(self, arr):
        new_arr = []

        for i in range(len(arr)):
            smallest = self.find(arr)
            new_arr.append(arr.pop(smallest))
    
        return new_arr