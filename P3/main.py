"""P3 - Cryptogrphy"""
from random import randint
from crypto_utils import (
    extended_gcd, modular_inverse, blocks_from_text, text_from_blocks, generate_random_prime
    )

class Cipher:
    """Cipher superclass all ciphers implement"""
    alphabet = [chr(i) for i in range(32, 127)]

    def encode(self, text, key):
        """Dummy method for superclass, should never be used"""
        return text + key

    def decode(self, text, key):
        """Dummy method for superclass, should never be used"""
        return text + key

    def verify(self, text, key):
        """Verifies if encoded text decodes to original text"""
        encoded = self.encode(text, key)
        return text == self.decode(encoded, key)

class Person:
    """Person super class sender and reciever implements"""
    def __init__(self, key, algorithm):
        self.key = key
        self.cipher = algorithm

    def set_key(self, key):
        """Sets the key this person should use"""
        self.key = key

    def get_key(self):
        """Returns the key this person is using"""
        return self.key


class Sender(Person):
    """Sender, encrypts a message for the reciever"""
    def operate_cipher(self, text):
        """Tells this sender to encode a message with its cipher"""
        return self.cipher.encode(text, self.key)

class Reciever(Person):
    """A reciever of an encrypted message,
    also generates rsa keys for sender and itself"""
    def __init__(self, key, algorithm):
        super().__init__(key, algorithm)
        self.key = key


    def operate_cipher(self, text):
        """Tells this reciever to decode a message with its cipher"""
        return self.cipher.decode(text, self.key)

    def rsa_keys(self):
        """Generates rsa keys for themselves and returns a public key"""
        prime_1, prime_2, product, phi, random, inverse = (0 ,0, 0, 0, 0, 0)
        while prime_1 == prime_2 or extended_gcd(random, phi)[0] != 1:
            prime_1 = generate_random_prime(8)
            prime_2 = generate_random_prime(8)
            product = prime_1 * prime_2
            phi = (prime_1 - 1)*(prime_2 - 1)
            random = randint(3, phi - 1)
            try:
                inverse = modular_inverse(random, phi)
            except:
                continue
        self.key = (product, inverse)
        return (product, random)

class Caesar(Cipher):
    """Ceasar cipher which uses a shift of each character when encoding"""
    def encode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) + key) % 95)] for i in text])

    def decode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) - key) % 95)] for i in text])

class Multiplicative(Cipher):
    """Multiplicative cipher which uses a multiplicative shift in encoding"""
    def encode(self, text, key):
        return ''.join([Cipher.alphabet[((Cipher.alphabet.index(i) * key) % 95)] for i in text])

    def decode(self, text, key):
        try:
            inversekey = modular_inverse(key, 95)
        except Exception:
            raise TypeError('Invalid keys for Multiplicative') from Exception
        return self.encode(text, inversekey)

class Affine(Cipher):
    """Affin cipher which first uses a Multiplicative encoding on the text, and then
    encodes that again with a ceasar cipher"""
    def __init__(self):
        self.caesar = Caesar()
        self.multi = Multiplicative()

    def encode(self, text, key):
        return self.caesar.encode(self.multi.encode(text, key[1]), key[0])

    def decode(self, text, key):
        return self.multi.decode(self.caesar.decode(text, key[0]), key[1])

class Unbreakable(Cipher):
    """'Unbreakable' cipher, every character is encoded with corresponding character from
    a key string (sequential)"""
    def encode(self, text, key):
        return ''.join([Cipher.alphabet[
            ((Cipher.alphabet.index(text[i]) + Cipher.alphabet.index(key[i % len(key)])) % 95)
            ] for i in range(len(text))])

    def decode(self, text, key):
        return ''.join([Cipher.alphabet[
            ((Cipher.alphabet.index(text[i]) - Cipher.alphabet.index(key[i % len(key)])) % 95)
            ] for i in range(len(text))])

class RSA(Cipher):
    """RSA encryption class with a public and private key"""
    def encode(self, text, key):
        return [(pow(i, key[1], key[0])) for i in blocks_from_text(text, 1)]

    def decode(self, text, key):
        tmp_1 = [pow(i, key[1], key[0]) for i in text]
        return text_from_blocks(tmp_1, 1)

class Hacker:
    """A hacker that takes a Cipher and a text and brute force decodes that
    text to return possible keys"""
    wordlist = [
        line.rstrip('\n') for line in open(__file__[:-7] + 'english_words.txt', 'r').readlines()
        ]

    def __init__(self, cipher):
        self.algorithm = cipher

    def break_text(self, text):
        """Tries to brute force decrypt a text given the Cipher"""
        tmp_1 = [modular_inverse(i, 95) for i in range(32, 127) if extended_gcd(i, 95)[0] == 1]

        if isinstance(self.algorithm, Caesar):
            return [i for i in range(32, 127) if self.algorithm.decode(text, i) in Hacker.wordlist]

        if isinstance(self.algorithm, Multiplicative):
            return [i for i in tmp_1 if self.algorithm.decode(text, i) in Hacker.wordlist]

        if isinstance(self.algorithm, Affine):
            return [
                (i, j) for i in tmp_1 for j in tmp_1 if self.algorithm.decode(
                    text, (i, j)
                    ) in Hacker.wordlist
                ]

        if isinstance(self.algorithm, Unbreakable):
            return [i for i in Hacker.wordlist if self.algorithm.decode(text, i) in Hacker.wordlist]

def main():
    """Main method"""

if __name__ == "__main__":
    main()
