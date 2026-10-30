
import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ==============================
# IPsec ESP + AH Simulation
# ==============================

print("======================================")
print("       IPsec VPN Simulation")
print("        ESP and AH Protocols")
print("======================================")

# Secret keys
aes_key = AESGCM.generate_key(bit_length=256)
auth_key = os.urandom(32)

aes = AESGCM(aes_key)

# ==============================
# ESP - Encryption
# ==============================

def esp_encrypt(data):
    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce,
        data.encode(),
        None
    )

    return nonce, encrypted


def esp_decrypt(nonce, encrypted):
    decrypted = aes.decrypt(
        nonce,
        encrypted,
        None
    )

    return decrypted.decode()


# ==============================
# AH - Authentication
# ==============================

def ah_create(data):
    return hmac.new(
        auth_key,
        data.encode(),
        hashlib.sha256
    ).hexdigest()


def ah_verify(data, tag):
    new_tag = ah_create(data)
    return hmac.compare_digest(new_tag, tag)


# ==============================
# Input
# ==============================

message = input("\nEnter message to send: ")

print("\nOriginal Message:")
print(message)


# =================================
# TRANSPORT MODE
# =================================

print("\n========== TRANSPORT MODE ==========")

# ESP protects the payload
nonce, encrypted_data = esp_encrypt(message)

print("\nESP:")
print("Encrypted Payload:", encrypted_data.hex())

# AH authenticates the payload
ah_tag = ah_create(message)

print("\nAH:")
print("Authentication Tag:", ah_tag)

# Verify authentication
if ah_verify(message, ah_tag):
    print("AH Verification: SUCCESS")
else:
    print("AH Verification: FAILED")

# Decrypt the payload
decrypted_message = esp_decrypt(
    nonce,
    encrypted_data
)

print("ESP Decrypted Payload:", decrypted_message)


# =================================
# TUNNEL MODE
# =================================

print("\n========== TUNNEL MODE ==========")

# Simulated complete IP packet
original_packet = (
    "Source IP: 10.0.0.1 | "
    "Destination IP: 10.0.0.2 | "
    "Data: " + message
)

print("\nOriginal IP Packet:")
print(original_packet)

# Encrypt the complete simulated packet
tunnel_nonce, tunnel_encrypted = esp_encrypt(
    original_packet
)

print("\nESP Tunnel Encryption:")
print("Encrypted Packet:", tunnel_encrypted.hex())

# Create AH authentication tag
tunnel_tag = ah_create(original_packet)

print("\nAH Tunnel Authentication:")
print("Authentication Tag:", tunnel_tag)

# Verify authentication
if ah_verify(original_packet, tunnel_tag):
    print("AH Verification: SUCCESS")
else:
    print("AH Verification: FAILED")

# Decrypt the tunnel packet
recovered_packet = esp_decrypt(
    tunnel_nonce,
    tunnel_encrypted
)

print("\nRecovered IP Packet:")
print(recovered_packet)


# =================================
# FINAL RESULT
# =================================

print("\n======================================")
print("                RESULT")
print("======================================")

if decrypted_message == message:
    print("ESP Encryption/Decryption: SUCCESS")

if ah_verify(message, ah_tag):
    print("AH Authentication: SUCCESS")

if recovered_packet == original_packet:
    print("Tunnel Mode Recovery: SUCCESS")

print("\nIPsec VPN simulation completed successfully.")
