
# Secure File Sharing System using Hybrid Cryptography,
# Access Control and IPsec Simulation
#
# Install:
# pip install cryptography

import os
import hmac
import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sympad
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
except ImportError:
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES


def title(t):
    print("\n" + "=" * 64)
    print(t)
    print("=" * 64)


# ============================================================
# PART 1: ACCESS CONTROL MATRIX
# ============================================================

title("PART 1: ACCESS CONTROL MATRIX")

matrix = {
    "Alice": {
        "report.txt": "rwx",
        "salary.txt": "rw-",
        "notes.txt": "r--"
    },
    "Bob": {
        "report.txt": "r--",
        "salary.txt": "---",
        "notes.txt": "rw-"
    },
    "Carol": {
        "report.txt": "r--",
        "salary.txt": "r--",
        "notes.txt": "---"
    }
}

files = ["report.txt", "salary.txt", "notes.txt"]

print("%-8s" % "User", end="")

for f in files:
    print("%-13s" % f, end="")

print()

for u in matrix:
    print("%-8s" % u, end="")

    for f in files:
        print("%-13s" % matrix[u][f], end="")

    print()


def check_access(user, file, right):
    permission = matrix.get(user, {}).get(file, "---")
    return right in permission


print("\nAccess requests:")

requests = [
    ("Alice", "report.txt", "w"),
    ("Bob", "salary.txt", "r"),
    ("Carol", "salary.txt", "r"),
    ("Bob", "report.txt", "w")
]

for user, file, right in requests:
    allowed = check_access(user, file, right)

    status = "GRANTED" if allowed else "DENIED"

    print(
        "%-6s wants '%s' on %-11s -> %s"
        % (user, right, file, status)
    )


# ============================================================
# PART 2: DISCRETE LOGARITHM USING BRUTE FORCE
# ============================================================

title("PART 2: DISCRETE LOGARITHM (BRUTE FORCE)")

g, p, h = 5, 23, 8

# Find x such that g^x mod p = h
value = 1
found = None

for x in range(p - 1):
    if value == h:
        found = x
        break

    value = (value * g) % p

print("Solve %d^x mod %d = %d" % (g, p, h))

if found is not None:
    print("Brute force result: x =", found)
    print("Verification:", pow(g, found, p))
else:
    print("No discrete logarithm found in the searched range.")

print("Attempts needed: at most p-1 =", p - 1)

print(
    "For a 127-bit prime, a brute-force search may require "
    "on the order of 2^127 attempts."
)

print("Brute-force discrete logarithms become computationally expensive.")


# ============================================================
# PART 3: DIFFIE-HELLMAN KEY EXCHANGE
# ============================================================

title("PART 3: DIFFIE-HELLMAN KEY EXCHANGE")

P = 2**127 - 1
G = 3

# Generate private keys
a = int.from_bytes(os.urandom(16), "big") % (P - 2) + 1
b = int.from_bytes(os.urandom(16), "big") % (P - 2) + 1

# Calculate public keys
A = pow(G, a, P)
B = pow(G, b, P)

# Calculate shared secrets
secret_alice = pow(B, a, P)
secret_bob = pow(A, b, P)

print("Alice public A =", hex(A)[:24] + "...")
print("Bob public B   =", hex(B)[:24] + "...")

print(
    "Shared secret equal on both sides:",
    secret_alice == secret_bob
)

# Convert the shared secret into a fixed-length byte sequence
shared_secret_bytes = secret_alice.to_bytes(
    (P.bit_length() + 7) // 8,
    "big"
)

# Derive a 256-bit session key
session_key = hashlib.sha256(shared_secret_bytes).digest()

print("Derived 256-bit session key:", session_key.hex()[:32] + "...")


# ============================================================
# PART 4: AES-256 FILE ENCRYPTION
# ============================================================

title("PART 4: AES-256 ENCRYPTION OF FILE")

file_data = (
    b"CONFIDENTIAL: Quarterly report - revenue up 12 percent."
)

aes_key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)

aes = AESGCM(aes_key)

cipher_text = aes.encrypt(nonce, file_data, None)

print("Plain text :", file_data.decode())
print("Cipher text:", cipher_text.hex()[:48] + "...")

decrypted_data = aes.decrypt(nonce, cipher_text, None)

print("Decrypted  :", decrypted_data.decode())


# ============================================================
# PART 5: DES ENCRYPTION AND DECRYPTION
# ============================================================

title("PART 5: DES ENCRYPTION AND DECRYPTION")

# Educational DES demonstration using TripleDES with
# the same key supplied for all three DES stages.
des_key = b"8bytekey"
triple_des_key = des_key * 3

iv = os.urandom(8)
msg = b"DES demo message"

# Apply PKCS7 padding for an 8-byte block cipher
padder = sympad.PKCS7(64).padder()

padded = padder.update(msg) + padder.finalize()

# Encryption
encryptor = Cipher(
    TripleDES(triple_des_key),
    modes.CBC(iv)
).encryptor()

des_ct = encryptor.update(padded) + encryptor.finalize()

# Decryption
decryptor = Cipher(
    TripleDES(triple_des_key),
    modes.CBC(iv)
).decryptor()

decrypted_padded = (
    decryptor.update(des_ct) + decryptor.finalize()
)

unpadder = sympad.PKCS7(64).unpadder()

des_pt = (
    unpadder.update(decrypted_padded) + unpadder.finalize()
)

print("Plain text :", msg.decode())
print("Cipher text:", des_ct.hex())
print("Decrypted  :", des_pt.decode())


# ============================================================
# PART 6: RSA + DIGITAL SIGNATURE + ENCRYPTION
# ============================================================

title("PART 6: RSA KEY WRAP + DIGITAL SIGNATURE (S/MIME STYLE)")

# Generate RSA key pairs
alice_priv = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

bob_priv = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

alice_pub = alice_priv.public_key()
bob_pub = bob_priv.public_key()

# RSA-PSS signature configuration
pss = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
)

# RSA-OAEP encryption configuration
oaep = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
)

# Alice signs the original file
signature = alice_priv.sign(
    file_data,
    pss,
    hashes.SHA256()
)

# Alice encrypts the AES key using Bob's public key
wrapped_key = bob_pub.encrypt(aes_key, oaep)

print("RSA key size : 2048 bits")
print("Signature (first 24 bytes):", signature.hex()[:48] + "...")
print("Wrapped AES key:", wrapped_key.hex()[:48] + "...")

# Bob decrypts the AES key
recv_key = bob_priv.decrypt(wrapped_key, oaep)

# Bob decrypts the encrypted file
recv_data = AESGCM(recv_key).decrypt(
    nonce,
    cipher_text,
    None
)

# Verify Alice's digital signature
try:
    alice_pub.verify(
        signature,
        recv_data,
        pss,
        hashes.SHA256()
    )

    print("Signature verification: VALID")

except Exception:
    print("Signature verification: INVALID")

# Test whether tampering is detected
try:
    alice_pub.verify(
        signature,
        recv_data + b"X",
        pss,
        hashes.SHA256()
    )

    print("Tampered file check: VALID")

except Exception:
    print("Tampered file check: INVALID (tampering detected)")

print("Bob received file:", recv_data.decode())


# ============================================================
# PART 7: IPsec ESP AND AH SIMULATION
# ============================================================

title("PART 7: IPsec SIMULATION - AH AND ESP")

# Derive separate authentication and encryption keys
auth_key = hashlib.sha256(
    session_key + b"auth"
).digest()

enc_key = hashlib.sha256(
    session_key + b"enc"
).digest()


def make_packet(src, dst, payload):
    return {
        "src": src,
        "dst": dst,
        "payload": payload
    }


# AH-style authentication simulation
def ah(pkt):
    data = (
        pkt["src"].encode()
        + pkt["dst"].encode()
        + pkt["payload"]
    )

    mac = hmac.new(
        auth_key,
        data,
        hashlib.sha256
    ).digest()

    return {
        **pkt,
        "AH_ICV": mac[:12].hex()
    }


def ah_verify(pkt):
    expected = ah(pkt)["AH_ICV"]
    return hmac.compare_digest(expected, pkt["AH_ICV"])


# ESP-style authenticated encryption simulation
def esp(pkt):
    n = os.urandom(12)

    associated_data = (
        pkt["src"].encode() + pkt["dst"].encode()
    )

    encrypted_payload = AESGCM(enc_key).encrypt(
        n,
        pkt["payload"],
        associated_data
    )

    return {
        "src": pkt["src"],
        "dst": pkt["dst"],
        "ESP_nonce": n.hex(),
        "ESP_payload": encrypted_payload.hex()
    }


# Tunnel mode: protect the original packet inside a new packet
def tunnel(pkt, gw1, gw2):
    inner_packet = (
        pkt["src"] + ">" + pkt["dst"] + ":"
    ).encode() + pkt["payload"]

    outer_packet = make_packet(
        gw1,
        gw2,
        inner_packet
    )

    encrypted_packet = esp(outer_packet)

    encrypted_packet["note"] = (
        "Original packet is encapsulated inside ESP"
    )

    return encrypted_packet


# Display packet information
def show(name, pkt):
    print("\n" + name)

    for k, v in pkt.items():
        if isinstance(v, bytes):
            display_value = v[:20].hex() + "..."
        elif isinstance(v, str) and len(v) > 48:
            display_value = v[:48] + "..."
        else:
            display_value = v

        print(" %-12s: %s" % (k, display_value))


original_packet = make_packet(
    "10.0.0.1",
    "10.0.1.1",
    file_data
)

show("Original packet", original_packet)

ah_packet = ah(original_packet)

show("[Captured] AH - transport mode", ah_packet)

print("AH integrity verification:", ah_verify(ah_packet))

esp_packet = esp(original_packet)

show("[Captured] ESP - transport mode", esp_packet)

tunnel_packet = tunnel(
    original_packet,
    "203.0.113.1",
    "203.0.113.2"
)

show("[Captured] ESP - tunnel mode", tunnel_packet)

print("\nAnalysis:")
print("AH -> Provides integrity/authentication in this simulation.")
print("ESP -> Encrypts and authenticates the payload.")
print("Tunnel mode -> Encapsulates the original packet inside ESP.")


# ============================================================
# PART 8: COMPLETE SECURE FILE SHARING
# ============================================================

title("PART 8: COMPLETE SECURE FILE SHARING")

sharing_requests = [
    ("Bob", "report.txt"),
    ("Carol", "report.txt"),
    ("Carol", "salary.txt"),
    ("Bob", "salary.txt")
]

for user, file in sharing_requests:

    if check_access(user, file, "r"):

        print(
            "%-6s requests %-11s -> ACCESS GRANTED "
            "-> encrypted with AES, AES key protected with RSA, "
            "and digital signature verified"
            % (user, file)
        )

    else:

        print(
            "%-6s requests %-11s -> ACCESS DENIED "
            "-> no data sent"
            % (user, file)
        )


# ============================================================
# FINAL RESULT
# ============================================================

title("FINAL RESULT")

print("1. Access Control Matrix: COMPLETED")
print("2. Discrete Logarithm: COMPLETED")
print("3. Diffie-Hellman Key Exchange: COMPLETED")
print("4. AES-256 Encryption: COMPLETED")
print("5. DES Demonstration: COMPLETED")
print("6. RSA and Digital Signature: COMPLETED")
print("7. IPsec ESP and AH Simulation: COMPLETED")
print("8. Secure File Sharing Access Check: COMPLETED")

print("\nSecure File Sharing System simulation completed.")
