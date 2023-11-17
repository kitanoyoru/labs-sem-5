import random


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_rsa_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q

    phi = (p - 1) * (q - 1)

    e = random.randint(1, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)

    d = pow(e, -1, phi)

    return (n, e), (n, d)


def encrypt(public_key, plain_text):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in plain_text]
    return encrypted_message


def decrypt(private_key, encrypted_message):
    n, d = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return "".join(decrypted_message)


if __name__ == "__main__":
    public_key, private_key = generate_rsa_keys(4)

    message = "bla bla bla"
    encrypted_message = encrypt(public_key, message)
    decrypted_message = decrypt(private_key, encrypted_message)

    print("Message: ", message)
    print("Encrypted Message: ", encrypted_message)
    print("Decrypted Message: ", message)
