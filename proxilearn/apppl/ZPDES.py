def generate_multi_item_change_question(priceA, priceB, change, valid_items, answer_type):
    #Génère une question et une solution pour rendre la monnaie lorsqu'il y a plusieurs articles.
    change_valid = False
    total_price = priceA + priceB
    while not change_valid:
        nb_item_select = random.choice([1, 2, 3])
        change_client = random.sample(change, nb_item_select)
        # Vérifie si le client donne suffisamment et si le rendu est valide
        if sum(change_client) >= total_price and (sum(change_client) - total_price) in valid_items:
            change_valid = True

    question = (
        f"""Tu es le marchand, rends la monnaie au client.\n
        Le premier article coûte {priceA}€.\n
        Le deuxième article coûte {priceB}€.\n
        Le client t'a donné {list(map(str, change_client))}."""
    )
    solution = sum(change_client) - total_price
    return question, solution, answer_type

priceA = random.choice(itemEasy + itemDifficult)
priceB = random.choice(itemEasy + itemDifficult)
# Dans le match statement
match self.difficulty:
    case Node.Difficulty.EASY:
        question, solution, answer_type = generate_multi_item_change_question(
            priceA, priceB, change, itemEasy, Node.AnswerType.INTEGER
        )

    case Node.Difficulty.HARD:
        question, solution, answer_type = generate_multi_item_change_question(
            priceA, priceB, change, itemDifficult, Node.AnswerType.LIST
        )

    case Node.Difficulty.VERYHARD:
        question, solution, answer_type = generate_multi_item_change_question(
            priceA, priceB, change, itemVeryDifficult, Node.AnswerType.LIST
        )


return {'question':question, 'solution':solution, 'answer_type':answer_type}