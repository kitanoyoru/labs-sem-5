import random
import itertools

from contants import ALPHABET

def generate_random_password(length: int) -> str:
    generated_string = "".join(random.choice(ALPHABET) for _ in range(length))
    return generated_string


def password_selection(target_password: str):
    for length in range(1, len(ALPHABET) + 1):
        for guess in itertools.product(ALPHABET, repeat=length):
            guessed_password = "".join(guess)
            if guessed_password == target_password:
                return

if __name__ == "__main__":
    password_length = int(input("Введите длину строки: "))
    password = generate_random_password(password_length)

    print("Сгенерированный пароль:", password)

    password_selection(password)
