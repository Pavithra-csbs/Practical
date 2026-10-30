
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Generate encryption key from password
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return kdf.derive(password.encode())


# Encrypt the file
def encrypt_file(input_file, output_file, password):
    with open(input_file, "rb") as file:
        data = file.read()

    salt = os.urandom(16)
    iv = os.urandom(16)

    key = generate_key(password, salt)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_file, "wb") as file:
        file.write(salt + iv + encrypted_data)

    print("\nFile encrypted successfully!")
    print("Encrypted file:", output_file)


# Decrypt the file
def decrypt_file(input_file, output_file, password):
    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    key = generate_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(output_file, "wb") as file:
        file.write(data)

    print("\nFile decrypted successfully!")
    print("Decrypted file:", output_file)


# Main program
print("================================")
print("     AES Secure File Transfer")
print("================================")

input_file = input("Enter file name: ")
password = input("Enter password: ")

encrypted_file = "encrypted_file.aes"
decrypted_file = "decrypted_file.txt"

try:
    encrypt_file(input_file, encrypted_file, password)
    decrypt_file(encrypted_file, decrypted_file, password)

    print("\nOriginal file :", input_file)
    print("Encrypted file:", encrypted_file)
    print("Decrypted file:", decrypted_file)

except FileNotFoundError:
    print("Error: Input file not found.")

except ValueError:
    print("Error: Invalid data or padding. Check the password.")

except Exception as e:
    print("Error:", e)
