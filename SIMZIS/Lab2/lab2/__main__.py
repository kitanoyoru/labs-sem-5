import random
import time
import math


ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

PASSWORD_LENGTH = 4

ROWS = 2
COLS = 2

def generate_random_text(alphabet, length):
    generated_string = "".join(random.choice(alphabet) for _ in range(length))
    return generated_string

def encrypt(text, rows, columns):
    text = text.replace(" ", "")
    encryptedText = ""

    table = []
    for i in range(rows):
        row = []
        for j in range(i * columns, i * columns + columns):
            if j < len(text):
                row.append(text[j])
            else:
                row.append("!")
        table.append(row)

    for i in range(columns):
        for j in range(rows):
            encryptedText += table[j][i]

    return encryptedText.strip(), table

def decrypt(encrypted_text, rows, columns):
    decrypted_text = ""
    table = []

    for i in range(rows):
        row = []
        for j in range(i, len(encrypted_text), rows):
            row.append(encrypted_text[j])
        table.append(row)

    for i in range(rows):
        for j in range(columns):
            decrypted_text += table[i][j]

    return decrypted_text.strip().replace("!", ""), table

def brute_force(encrypted_text, text):
    max_rows = math.ceil(len(encrypted_text) / COLS)
    max_columns = math.ceil(len(encrypted_text) / ROWS)

    best_decryption = ""
    best_key = ""

    for rows in range(1, max_rows + 1):
        for columns in range(1, max_columns + 1):
            decrypted_text, _ = decrypt(encrypted_text, rows, columns)

            if decrypted_text.lower() == text.lower():
                best_decryption = decrypted_text
                best_key = f"{rows}x{columns}"
                break

    return best_decryption, best_key

if __name__ == "__main__":
    text = generate_random_text(ALPHABET, PASSWORD_LENGTH)

    print("Initial password:", text)

    print()

    encrypted_text, encrypted_table = encrypt(text, ROWS, COLS)
    decrypted_text, decrypted_table = decrypt(encrypted_text, ROWS, COLS)

    print("Encrypted password:", encrypted_text)
    print("Encrypted table:", encrypted_table)

    print()

    print("Decrypted password:", decrypted_text)
    print("Decrypted table:", decrypted_table)

    print()

    start = time.time()
    best_decryption, best_key = brute_force(encrypted_text, text)
    end = time.time()

    print("Brute-Force result:", best_decryption, best_key, f"({end-start})")


    



