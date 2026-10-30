
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

print("===== S/MIME Digital Signature and Encryption =====")

# Generate sender RSA key pair
sender_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
sender_public_key = sender_private_key.public_key()

# Generate receiver RSA key pair
receiver_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
receiver_public_key = receiver_private_key.public_key()

# Get message
message = input("Enter confidential message: ")
message_bytes = message.encode("utf-8")

# Create digital signature
signature = sender_private_key.sign(
    message_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print("Digital signature created successfully.")

# Generate AES key and IV
aes_key = os.urandom(32)
iv = os.urandom(16)

# Apply PKCS7 padding
padding_length = 16 - (len(message_bytes) % 16)
padded_message = message_bytes + bytes([padding_length]) * padding_length

# AES encryption
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
encryptor = cipher.encryptor()

encrypted_message = (
    encryptor.update(padded_message) + encryptor.finalize()
)

# Encrypt AES key using receiver's RSA public key
encrypted_aes_key = receiver_public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message encrypted successfully.")
print("Encrypted Message:", base64.b64encode(encrypted_message).decode())
print("Encrypted AES Key:", base64.b64encode(encrypted_aes_key).decode())

# Decryption: recover AES key
decrypted_aes_key = receiver_private_key.decrypt(
    encrypted_aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# AES decryption
cipher = Cipher(algorithms.AES(decrypted_aes_key), modes.CBC(iv))
decryptor = cipher.decryptor()

decrypted_padded = (
    decryptor.update(encrypted_message) + decryptor.finalize()
)

# Remove padding
padding_length = decrypted_padded[-1]
decrypted_message = decrypted_padded[:-padding_length]

# Verify digital signature
try:
    sender_public_key.verify(
        signature,
        decrypted_message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    signature_status = "VALID"

except Exception:
    signature_status = "INVALID"

# Display results
print("\n===== Receiver Side =====")
print("Decrypted Message:", decrypted_message.decode("utf-8"))
print("Digital Signature:", signature_status)

if signature_status == "VALID":
    print("Secure communication successful!")
else:
    print("Signature verification failed!")
