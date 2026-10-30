
import math

# Choose two prime numbers
p = 61
q = 53

# Calculate n
n = p * q

# Calculate Euler's Totient
phi = (p - 1) * (q - 1)

# Choose public exponent
e = 17

# Calculate private exponent
d = pow(e, -1, phi)

print("===== RSA Encryption and Decryption =====")
print("Public Key :", (e, n))
print("Private Key:", (d, n))

# Get message
message = input("\nEnter confidential message: ")

# Convert message characters to numbers
message_numbers = [ord(char) for char in message]

# Encryption
encrypted = [pow(m, e, n) for m in message_numbers]
print("\nEncrypted message:", encrypted)

# Decryption
decrypted_numbers = [pow(c, d, n) for c in encrypted]

# Convert numbers back to characters
decrypted = ''.join(chr(m) for m in decrypted_numbers)

print("Decrypted message:", decrypted)
