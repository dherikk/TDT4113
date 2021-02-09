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
        self.key = key

    
    def operate_cipher(self, text):
        return self.Cipher.decode(text, self.key)

    def RSA_keys(self):
        p, q, n, φ, e, d = (0 ,0, 0, 0, 0, 0)
        while p == q or extended_gcd(e, φ)[0] != 1:
            p = generate_random_prime(8)
            q = generate_random_prime(8)
            n = p  *q
            φ = (p - 1)*(q - 1)
            e = random.randint(3, φ - 1)
            try:
                d = modular_inverse(e, φ)
            except:
                continue
        self.key = (n, d)
        return (n, e)

class Caesar(Cipher):

    def encode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) + key) % 95)] for i in text])

    def decode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) - key) % 95)] for i in text])
        
class Multiplicative(Cipher):
   
    def encode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) * key) % 95)] for i in text])

    def decode(self, text, key):
        try:
            inversekey = modular_inverse(key, 95)
        except Exception:
            print('Invalid key for Multiplicative')
        return self.encode(text, inversekey)

class Affine(Cipher):

    def __init__(self):
        self.caesar = Caesar()
        self.multi = Multiplicative()
        
    def encode(self, text, key):
        return self.caesar.encode(self.multi.encode(text, key[1]), key[0])

    def decode(self, text, key):
        return self.multi.decode(self.caesar.decode(text, key[0]), key[1])

class Unbreakable(Cipher):
        
    def encode(self, text, key):
        return ''.join([Cipher.alphabet[
            ((Cipher.alphabet.index(text[i]) + Cipher.alphabet.index(key[i % len(key)])) % 95)
            ] for i in range(len(text))])

    def decode(self, text, key):
        return ''.join([Cipher.alphabet[
            ((Cipher.alphabet.index(text[i]) - Cipher.alphabet.index(key[i % len(key)])) % 95)
            ] for i in range(len(text))])
    
class RSA(Cipher):

    def encode(self, text, key):
        return [(pow(i, key[1], key[0])) for i in blocks_from_text(text, 1)]

    def decode(self, text, key):
        tmp_1 = [pow(i, key[1], key[0]) for i in text]
        return text_from_blocks(tmp_1, 1)
        
class Hacker:

    wordlist = [
        line.rstrip('\n') for line in open(__file__[:-7] + 'english_words.txt', 'r').readlines()
        ]

    def __init__(self, Cipher):
        self.algorithm = Cipher

    def break_text(self, text):

        if isinstance(self.algorithm, Caesar):
            return [i for i in range(32, 127) if self.algorithm.decode(text, i) in Hacker.wordlist]
            
        elif isinstance(self.algorithm, Multiplicative):
            tmp_1 = [modular_inverse(i, 95) for i in range(32, 127) if extended_gcd(i, 95)[0] == 1]
            return [i for i in tmp_1 if self.algorithm.decode(text, i) in Hacker.wordlist]
            
        elif isinstance(self.algorithm, Affine):
            return [(i, j) for i in range(32, 127) for j in range(32, 127) if self.algorithm.decode(text, (i, j)) in Hacker.wordlist]

        elif isinstance(self.algorithm, Unbreakable):
            return [i for i in Hacker.wordlist if self.algorithm.decode(text, i) in Hacker.wordlist]


def main():
    Ca = Caesar()
    Mu = Multiplicative()
    Af = Affine()
    Ub = Unbreakable()
    """key_1 = 33
    key_2 = [322, 2323]
    key_3 = 'wefwefwdsf'
    encoded = Ca.encode('test   ~~', key_1)
    print(encoded)
    decoded = Ca.decode(encoded, key_1)
    print(decoded)
    rsa = RSA()
    P1.set_key(P2.RSA_keys())
    encoded = P1.operate_cipher('')
    print(encoded)
    decoded = P2.operate_cipher(encoded)
    print(decoded)"""
    P1 = Sender(662234, Ca)
    P2 = Reciever(662234, Ca)
    encoded = P1.operate_cipher('test   ~~')
    decoded = P2.operate_cipher(encoded)
    print(decoded)
    
if __name__ == "__main__":
    main()

        

    