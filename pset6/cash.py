from cs50 import get_float

while True:
    owed = round(get_float("Change owed: ") * 100)
    
    if owed > 0:
        break
    
coins = [25, 10, 5, 1]

change = 0

for c in coins:
    if owed == 0:
        break
    change += owed // c
    owed = owed % c
    
print(change)
