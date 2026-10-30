
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Get input
message = input("Enter the message: ")
key = input("Enter 8-character key: ")

# Check key length
if len(key) != 8:
    print("Error: Key must be exactly 8 characters.")
    exit()

# Convert key to bytes
key = key.encode()

# Convert message to bytes
data = message.encode()

# Create DES cipher
cipher = DES.new(key, DES.MODE_ECB)

# Encrypt
encrypted = cipher.encrypt(pad(data, DES.block_size))
print("\nEncrypted data:", encrypted.hex())

# Decrypt
cipher = DES.new(key, DES.MODE_ECB)

decrypted = unpad(
    cipher.decrypt(encrypted),
    DES.block_size
)

print("Decrypted data:", decrypted.decode())
