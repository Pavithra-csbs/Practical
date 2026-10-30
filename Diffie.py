
# Diffie-Hellman Key Exchange Without Built-in Functions

# Public values
p = 23
g = 5

# Private keys
a = 6
b = 15

# Alice public key calculation
A = 1
for i in range(a):
    A = (A * g) % p

# Bob public key calculation
B = 1
for i in range(b):
    B = (B * g) % p

# Alice shared secret calculation
alice_shared_key = 1
for i in range(a):
    alice_shared_key = (alice_shared_key * B) % p

# Bob shared secret calculation
bob_shared_key = 1
for i in range(b):
    bob_shared_key = (bob_shared_key * A) % p

# Display results
print("Diffie-Hellman Key Exchange")
print("Public Prime:", p)
print("Public Generator:", g)
print("Alice Public Key:", A)
print("Bob Public Key:", B)
print("Alice Shared Secret:", alice_shared_key)
print("Bob Shared Secret:", bob_shared_key)

if alice_shared_key == bob_shared_key:
    print("Shared key successfully established!")
else:
    print("Key exchange failed!")
