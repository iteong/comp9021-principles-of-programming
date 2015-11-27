# Encrypts and decrypts the contents of a file using the RSA cryptographic system.
#
# Written by Eric Martin for COMP9021


from random import randint
from math import log
from primes import list_of_primes_up_to


class RSA:
    def __init__(self):
        self.encryption_exponent = 65537
        self.modulus, totative_count = self.generate_modulus_and_totative_count()
        self.decryption_exponent = self.generate_decryption_exponent(totative_count)
        self.chunk_size = int(log(self.modulus, 1000))

    def public_key(self):
        return self.modulus, self.encryption_exponent

    def private_key(self):
        return self.modulus, self.decryption_exponent

    def generate_modulus_and_totative_count(self):
        b1 = randint(100000, 1000000)
        b2 = randint(2 * b1, 10 * b1)
        primes = list_of_primes_up_to(b2)
        q = primes.pop()
        p = primes.pop()
        while p > b1:
            p = primes.pop()
        return p * q, (p - 1) * (q - 1)

    def generate_decryption_exponent(self, totative_count):
        return self.bezout_coefficients(totative_count, self.encryption_exponent)[1] % totative_count

    # Returns a pair (x, y) with ax + by = gcd(a, b)          
    def bezout_coefficients(self, a, b):
        if b == 0:
            return 1, 0
        x, y = self.bezout_coefficients(b, a % b)
        return y, x - (a // b) * y

    # Returns x^k (mod p)
    def modular_exponentiation(self, x, n, p):
        if n == 0:
            return 1
        y = self.modular_exponentiation((x * x) % p, n // 2, p)
        if n % 2:
            y = (y * x) % p
        return y

    def encrypt(self, filename):
        try:
            file_to_encode = open(filename, 'r')
        except:
            print('Could not open file to encode.')
            return
        try:
            encoded_file = open(filename + '.encoded', 'w')
        except:
            print('Could not create encoded file.')
            return
        chunk_to_encode = ''.join(['{:03d}'.format(ord(i)) for i in file_to_encode.read(self.chunk_size)])
        while chunk_to_encode:
            coded_number = self.modular_exponentiation(int(chunk_to_encode), self.encryption_exponent, self.modulus)
            print(coded_number, file = encoded_file)
            chunk_to_encode = ''.join(['{:03d}'.format(ord(i)) for i in file_to_encode.read(self.chunk_size)])
        file_to_encode.close()
        encoded_file.close()

    def decrypt(self, filename):
        try:
            file_to_decode = open(filename, 'r')
        except:
            print('Could not open file to decode.')
            return
        number_to_decode = file_to_decode.readline()[:-1]
        while number_to_decode:
            decoded_number = self.modular_exponentiation(int(number_to_decode), self.decryption_exponent, self.modulus)
            chunk_to_decode = str('%0*d' % (self.chunk_size * 3, decoded_number))
            while chunk_to_decode:
                print('%c' % int(chunk_to_decode[:3]), end = '')
                chunk_to_decode = chunk_to_decode[3:]
            number_to_decode = file_to_decode.readline()[:-1]
            
        file_to_decode.close()
    

    
