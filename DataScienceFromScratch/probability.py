import random as rand

def randomKid():
    return rand.choice(["boy", "girl"])

both_girls = 0
older_girl = 0
either_girl = 0

rand.seed(0)

for _ in range(10000):
    younger = randomKid()
    older = randomKid()

    if(older == "girl"):
        older_girl += 1
    
    if(older == "girl" and younger == "girl"):
        both_girls += 1

    if(older == "girl" or younger == "girl"):
        either_girl += 1

print("P(both | older): ", both_girls / older_girl)
print("P(both | either): ", both_girls / either_girl)