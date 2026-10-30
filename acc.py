
num_users = int(input("Enter number of employees: "))
users = []

for i in range(num_users):
    user = input(f"Enter employee {i+1} name: ")
    users.append(user)

num_objects = int(input("\nEnter number of company resources: "))
objects = []

for i in range(num_objects):
    obj = input(f"Enter resource {i+1} name: ")
    objects.append(obj)

matrix = {}

print("\nEnter access rights:")
print("Examples: R, W, X, RW, RX, RWX, None\n")

for user in users:
    matrix[user] = {}
    for obj in objects:
        access = input(f"{user}'s access to {obj}: ").upper()
        matrix[user][obj] = access

print("\n========== ACCESS CONTROL MATRIX ==========")

print(f"{'Employee':<15}", end="")

for obj in objects:
    print(f"{obj:<15}", end="")
print()

for user in users:
    print(f"{user:<15}", end="")
    for obj in objects:
        print(f"{matrix[user][obj]:<15}", end="")
    print()