# ---------- Variable Assignments ----------
x = 5
y = 10
z = -3
a = 0
b = 0

# ---------- If / Elif / Else ----------
if x > 0 and y < 20:
    a = x + y
elif x == 0 or not z < 0:
    a = x - y
else:
    a = x * y

if not x:
    b = z
elif x < y:
    b = z + x
else:
    b = z - y

# ---------- For loops ----------
# range(stop)
for i in range(3):
    x = x + i

# range(start, stop)
for j in range(2, 5):
    y = y * j

# range(start, stop, step)
for k in range(5, 1, -1):
    z = z - k

# range with step = 2
for m in range(0, 10, 2):
    a = a + m

# combined with if inside loop
for n in range(5):
    if n % 2 == 0:
        b = b + n
    else:
        b = b - n
