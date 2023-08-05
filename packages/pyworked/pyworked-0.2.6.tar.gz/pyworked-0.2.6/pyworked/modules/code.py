import random

alphabet = {

    'a': '1134', 
    'b': '2341', 
    'c': '1514', 
    'd': '74234', 
    'e': '2346', 
    'f': '8726', 
    'g': '8934', 
    'h': '3119', 
    'i': '2574', 
    'j': '9344', 
    'k': '1234', 
    'l': '8901', 
    'm': '6713', 
    'n': '7892', 
    'o': '2372', 
    'p': '6438', 
    'q': '2364', 
    'r': '1927', 
    's': '3478', 
    't': '2830', 
    'u': '7364', 
    'v': '9873', 
    'w': '2034', 
    'x': '6712', 
    'y': '6183', 
    'z': '1264', 
    '-': '8193',
    '_': '1297', 
    '.': '2739', 
    ',': '2983',
}


alphabet1 = {

    1134.0: 'a', 
    2341.0: 'b', 
    1514.0: 'c', 
    74234.0: 'd', 
    2346.0: 'e', 
    8726.0: 'f', 
    8934.0: 'g', 
    3119.0: 'h', 
    2574.0: 'i', 
    9344.0: 'j', 
    1234.0: 'k', 
    8901.0: 'l', 
    6713.0: 'm', 
    7892.0: 'n', 
    2372.0: 'o', 
    6438.0: 'p', 
    2364.0: 'q', 
    1927.0: 'r', 
    3478.0: 's', 
    2830.0: 't', 
    7364.0: 'u', 
    9873.0: 'v', 
    2034.0: 'w', 
    6712.0: 'x', 
    6183.0: 'y', 
    1264.0: 'z', 
    8193.0: '-', 
    2739.0: '.',
    2983.0: ','
}


class Shifr:

    def __init__(self):
        self.key = []
        self.message = []
        self.encryption_message = []
        self.long_message = 0


    def key_gen(self):
        for self.i in self.message:
            self.long_message += 1

        for self.i in range(self.long_message):
            self.rand = random.randint(10, 101)
            self.key.append(self.rand)

        return(self.key)


    def  create_message(self, message):
        message.lower()
        for i in message:
            k = alphabet.get(i)
            self.message.append(k)


    def encryption(self):
        for self.i in range(len(self.message)):

            self.one_encryption_message = int(self.message[self.i]) * self.key[self.i]
            self.encryption_message.append(int(self.one_encryption_message))

        return self.encryption_message



class DeShifr:

    def __init__(self):
        self.decryption_message = []
        self.finally_message = []

    def decryption(self, keys, message):
        for self.i in range(len(message)):
            self.one_decryption_message = int(message[self.i]) / int(keys[self.i])
            self.decryption_message.append(self.one_decryption_message)


    def message_formation(self):
        for self.i in self.decryption_message:
            self.k = alphabet1.get(self.i)
            self.finally_message.append(self.k)

        return self.finally_message


'''   
EXAMPLE: 

a = Shifr()
a.create_message("hello")   # create_message
print(a.key_gen())      # create_keys
print(a.encryption())   # print encryption message

# -------------------------------------------------------------------------------------

b = DeShifr()
b.decryption([51, 24, 17, 85, 10], [159069, 56304, 151317, 756585, 23720]))   # data input
print(b.message_formation())    # receiving a decrypted message

'''
