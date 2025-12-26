def add(a, b):
    return a + b

def square(x):
    return x * x

# ---- Constant Folding Demo ----
x = 2 + 3
y = 10 * 4
z = x + y

# ---- Dead Code Elimination Demo ----
unused = 999
temp = 12345  # removed by DCE

# ---- Function Calls ----
result = add(z, 5)
squared = square(result)

# ---- If / Else Demo ----
if result > 40:
    flag = 1
else:
    flag = 0

# ---- Loop Demo ----
sum = 0
for i in range(0, 5):
    sum = sum + i

# ---- Conditional Output ----
if flag == 1:
    print(squared)
else:
    print(result)

print(sum)
