import os
import random
import math
import numpy as np

class MathModule:
    def __init__(self):
        self.__data_directory = "./data"
        self.__primes_file = "primes.txt"
        self.__generated_primes_count = 100000

        self.__generate_primes_file()

        # Load first few hundred primes
        self.__first_primes = self.__load_first_few_hundred_primes(500)

    def generate_large_prime(self):
        '''
        This method generates a large prime,
        which length is between 1024 bits and 2048 bits
        '''

        n = 1024
        prime_candidate = 0
        while True:
            prime_candidate = self.__get_low_level_prime(1024)
            if self.__is_miller_rabin_passed(prime_candidate):
                break
        return prime_candidate

    def choose_random_primes(self):
            '''
            This method chooses two random primes from
            the primes.txt file, which cointains 100k 
            pre-generated prime numbers.
            Since the prime numbers should be relatively
            large, this function chooses the random prime
            from the subset of the pre-generated primes.
            '''

            try:
                filename = self.__data_directory + "/" + self.__primes_file
                file = open(filename, "r")

                # Choosing two relatively big prime numbers from the generated file
                rand_1 = random.randint(int(0.8 * self.__generated_primes_count), self.__generated_primes_count)
                rand_2 = random.randint(int(0.8 * self.__generated_primes_count), self.__generated_primes_count)

                lines = file.read().splitlines()

                prime_1 = int(lines[rand_1])
                prime_2 = int(lines[rand_2])

                file.close()

                return (prime_1, prime_2)

            except FileNotFoundError:
                print(f"File \"{filename}\" not found.")

            else:
                print(f"Unexpected error while opening \"{filename}\"")

    def calculate_multiplicative_inverse(self, e, phi):
        '''
        This method returns the multiplicative inverse of number n
        using the Extended Euclidean algorithm.
        '''

        gcd, x, y = self.__extended_gcd(e, phi)
        # If the coefficient x turns out to be negative
        # then we increase it by phi value, which is the
        # modulus (e * d ≅ 1 (mod phi)). This works, because
        # e * d ≅ 1 (mod phi) ≅ e * (d + phi) (mod phi).
        # We do not want d to be negative, since it will
        # be used as a exponent in decrypting.
        if x < 0:
            x += phi
        return x

    def __generate_n_bit_random(self, n):
        return random.randrange(2 ** (n - 1) + 1, 2 ** (n) - 1)

    def __get_low_level_prime(self, n):
        '''
        Generate a prime candidate divisible by first primes.
        '''

        while True:
            # Obtain a random n-bit number
            prime_candidate = self.__generate_n_bit_random(n)

            # Low-level primality testing
            for divisor in self.__first_primes:
                if prime_candidate % divisor == 0 and divisor ** 2 <= prime_candidate:
                    break                
                else:
                    return prime_candidate

    def __is_miller_rabin_passed(self, candidate):
        '''
        This method is an implementation of high-level Rabin Miller Primality Test.
        When a prime candidate passes the low-level test it is then tested again
        with the Rabin Miller Test. Checking if a chosen extremely large number
        is prime in a deterministic way is highly impractical. A probabilistic
        approach is preferred. If an inputted value passes a single iteration of
        the Rabin Miller test, the probability of the number being prime is 75%.
        When the test is passed a number of times it can be considered to be a prime
        with a satisfactory level of probability.
        The error probability has to be less than (1/2)^128. 
        '''

        # Running 20 iterations of Rabin Miller Primality test
        trials_count = 20
        max_div_by_two = 0
        even_component = candidate - 1

        while even_component % 2 == 0:
            even_component >>= 1
            max_div_by_two += 1
        assert(2 ** max_div_by_two * even_component == candidate - 1)

        def trial_composite(round_tester):
            if pow(round_tester, even_component, candidate) == 1:
                return False
            for i in range(max_div_by_two):
                if pow(round_tester, 2 ** i * even_component, candidate) == candidate - 1:
                    return False
            return True

        for i in range(trials_count):
            round_tester = random.randrange(2, candidate)
            if trial_composite(round_tester):
                return False
        return True
    
    def __is_prime(self, n):
        '''
        All primes are not divisible by 2 (they are odd numbers).
        All primes greater than 3 are of the form: 6n ± 1, and because
        of that we start by checking the divisors from d = 5 (inclusive).
        Then, we test whether n is divisible by d and d + 2,
        each time we increment d by 6.
        '''

        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        r = int(n ** 0.5)
        d = 5
        while d <= r:
            if n % d == 0:
                return False
            if n % (d + 2) == 0:
                return False
            d += 6
        return True

    def __extended_gcd(self, a ,b):
        '''
        This method returns the greatest commond divisor of
        numbers a and b, and the coefficients x and y from the
        Bezout's identity (ax + by = gcd(a, b))  
        '''
        
        prev_x, x = 1, 0
        prev_y, y = 0, 1
        while b:
            q = a // b
            x, prev_x = prev_x - q * x, x
            y, prev_y = prev_y - q * y, y
            a, b = b, a % b
        return a, prev_x, prev_y

    def __extended_gcd_rec(self, a ,b):
        '''
        This recursive method returns the greatest commond divisor of
        numbers a and b, and the coefficients x and y from the
        Bezout's identity (ax + by = gcd(a, b))  
        '''

        if a == 0:
            return b, 0, 1
        gcd, x_1, y_1 = self.__extended_gcd_rec(b % a, a)
        x = y_1 - (b // a) * x_1
        y = x_1
        return gcd, x, y

    def __load_first_few_hundred_primes(self, primes_count):
        primes = list()
        n_primes = 0
        n = 1
        while n_primes < primes_count:
            if self.__is_prime(n):
                n_primes += 1
                primes.append(n)
            n += 1
        return primes

    def __generate_primes_file(self):
        '''
        This method creates a file which contains
        pre-generated prime numbers, whose quantity
        is denoted by the __generated_primes_count field.
        '''

        # Check whether the data directory exists
        if not os.path.isdir(self.__data_directory):
            os.mkdir(self.__data_directory)

        filename = self.__data_directory + "/" + self.__primes_file
        
        # Check whether the file already exists and has at least the chosen amount of prime numbers
        # If the file has more lines than the chosen number of primes to generate than we skip
        # generating the same file with fewer prime numbers.
        if os.path.isfile(filename):
            file = open(filename, "r")
            lines = file.read().splitlines()
            if len(lines) >= self.__generated_primes_count:
                file.close()
                return
            file.close()

        # Generating prime numbers and saving them in a file
        print("[INFO] Generating a file with", self.__generated_primes_count, "prime numbers.")
        file = open(filename, "w")
        n_primes = 0
        n = 1
        while n_primes < self.__generated_primes_count:
            if self.__is_prime(n):
                n_primes += 1
                file.write(str(n) + "\n")
            n += 1
        file.close()
        print("[INFO] Generation complete.")