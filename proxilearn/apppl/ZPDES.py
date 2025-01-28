import random

question = {"question": str(), "solution": str(), "answer_type": str()}
change = [10,5,2,1,0.5,0.2,0.1] #pièces et billets disponibles
itemEasy = [1,2,5,10] #à lecture directe, c’est-à-dire si une pièce ou un billet de la valeur de ce montant existe
itemDifficult = [3,4,6,7,8,9,11,12,13,14,15,16,17,18,19] #combiner plusieurs monnaie
itemVeryDifficult = [] #combiner une pièce ou un billet avec une pièce de centime
for k in range (19) :
    for i in range (4,7):
        itemVeryDifficult.append(k+change[i])
print(itemVeryDifficult)

def calculate_solution(price, change):
    # Calcule la solution en décomposant le prix avec les valeurs disponibles dans change.
    solution = []
    left_to_pay = price
    i = 0
    while i < len(change) and left_to_pay > 0:
        if left_to_pay - change[i] >= 0:
            left_to_pay -= change[i]
            solution.append(change[i])
        else:
            i += 1  # Passe à une valeur plus petite si la valeur actuelle est trop grande
    return solution


##EASY
price = random.choice(itemEasy + itemDifficult)
change_valid = False
while not change_valid:
    change_client = random.choice(itemEasy + itemDifficult)
    # Vérifie si le client donne suffisamment et si le rendu est valide
    if change_client >= price and (change_client - price) in itemEasy:
        change_valid = True

question = (
    f"""Tu es le marchand, rends la monnaie au client.\n
    Le premier article coûte {price}€.\n
    Le client t'a donné {change_client}."""
)
solution = change_client - price
print(f"EASY // question:{question}, solution:{solution}")


##HARD
price = random.choice(itemEasy + itemDifficult)
change_valid = False
while not change_valid:
    items = itemEasy + itemDifficult
    change_client = random.choice(items)
    # Vérifie si le client donne suffisamment et si le rendu est valide
    if change_client >= price and (change_client - price) in itemDifficult:
        change_valid = True
    else :
        items.remove(change_client)

question = (
    f"""Tu es le marchand, rends la monnaie au client.\n
    Le premier article coûte {price}€.\n
    Le client t'a donné {change_client}."""
)
rendu = change_client - price
solution = calculate_solution(rendu, change)
print(f"HARD // question:{question}, solution:{solution}")


##VEYHARD
price = random.choice(itemEasy + itemDifficult)
print(f"price{price}")
change_valid = False
while not change_valid:
    items = itemVeryDifficult
    change_client = random.choice(items)
    print(f"change_client{change_client}")
    # Vérifie si le client donne suffisamment et si le rendu est valide
    if change_client >= price and (change_client - price) in itemVeryDifficult:
        change_valid = True
    else :
        items.remove(change_client)

question = (
    f"""Tu es le marchand, rends la monnaie au client.\n
    Le premier article coûte {price}€.\n
    Le client t'a donné {change_client}."""
)
rendu = change_client - price
solution = calculate_solution(rendu, change)
print(f"VERYDIFFICULT // question:{question}, solution:{solution}")

