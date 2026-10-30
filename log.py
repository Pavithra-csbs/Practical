
# Discrete Logarithm using Brute Force

g = int(input("Enter base (g): "))
h = int(input("Enter target value (h): "))
p = int(input("Enter prime modulus (p): "))

value = 1
found = False

for x in range(p - 1):
    if value == h:
        print("\nDiscrete logarithm x =", x)
        print(f"Verification: {g}^{x} mod {p} =", pow(g, x, p))
        found = True
        break

    value = (value * g) % p

if not found:
    print("\nNo discrete logarithm found.")

print("\nComputational Challenge:")
print("Brute-force method may require up to p-1 attempts.")
print("For very large prime moduli, this becomes computationally expensive.")