from crypto_utils import *

class Cipher:

    alphabet = [chr(i) for i in range(32, 127)]
        
    def encode(self, text, key):
        return text

    def decode(self, text, key):
        return text

    def verify(self, text, key):
        encoded = self.encode(text, key)
        return text == self.decode(encoded, key)

class Person:

    def __init__(self, key, algorithm):
        self.key = key
        self.Cipher = algorithm

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key


class Sender(Person):

    def __init__(self, key, algorithm):
        super().__init__(key, algorithm)

    def operate_cipher(self, text):
        return self.Cipher.encode(text, self.key)

class Reciever(Person):

    def __init__(self, key, algorithm):
        super().__init__(key, algorithm)

    def operate_cipher(self, text):
        return self.Cipher.decode(text, self.key)

class Hacker(Person):

    def __init__(self, key, algorithm):
        super().__init__(key, algorithm)

class Caesar(Cipher):

    def __init__(self, key):
        self.key = key

    def encode(self, text):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) + self.key) % 95)] for i in text])

    def decode(self, text):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) - self.key) % 95)] for i in text])
        
class Multiplicative(Cipher):
    
    def __init__(self, key):
        self.key = key
        try:
            self.inverse = modular_inverse(key, 95)
        except Exception:
            print('Invalid key for Multiplicative')

    def encode(self, text):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) * self.key) % 95)] for i in text])

    def decode(self, text):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) * self.inverse) % 95)] for i in text])

class Affine(Cipher):

    def __init__(self, key):
        self.caesar = Caesar(key[0]) #Caesar
        self.multiplicative = Multiplicative(key[1]) #Multi
        
    def encode(self, text):
        return self.caesar.encode(self.multiplicative.encode(text))

    def decode(self, text):
        return self.multiplicative.decode(self.caesar.decode(text))

class Unbreakable(Cipher):

    def __init__(self, key):
        self.key = key
        
    def encode(self, text):
        ## Endr denne
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) + self.key) % 95)] for i in text])

    def decode(self, text):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) - self.key) % 95)] for i in text])
    

def main():
    """Main method"""
    Af = Affine((4,2))
    encoded = Af.encode('test   ~~')
    print(encoded)
    decoded = Af.decode(encoded)
    print(decoded)
    
if __name__ == "__main__":
    main()

        

    