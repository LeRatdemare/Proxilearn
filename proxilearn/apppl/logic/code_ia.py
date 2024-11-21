from apppl.logic.category import Category
from apppl.logic.difficulty import Difficulty
import random

class Node:

    def __init__(self, category: Category, difficulty: int, is_available: bool= False, previous_trials: list[dict] = []):
        self.category: Category = category
        self.difficulty: int = difficulty
        self.is_available: bool = is_available
        self.previous_trials: list[dict[str, str, str, str]] = previous_trials # [{question, solution, answer, distance}, ...]
    
    def generate_question(self) -> dict[str, str]:
        """
        Génère une question aléatoire en fonction de la catégorie et de la difficulté de l'exercice.

        return: question sous la forme {str(question), str(solution)}
        """
        question = {"question": str(), "solution": str()}
        change = [10,5,2,1] #pièces et billets disponibles, on pourra en rajouter plus tard
        itemEasy = [1,2,5,10] #à lecture directe, c’est-à-dire si une pièce ou un billet de la valeur de ce montant existe
        itemDifficult = [3,4,6,7,8,9,11,12,13,14,15,16,17,18,19] #combiner plusieurs objet

        match self.category:
            #acheter et payer un objet
            case Category.TypeM:
                match self.difficulty:
                    case Difficulty.EASY:
                       price = random.choice(itemEasy)
                       question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le jeu coûte {price}€."
                       solution = price                      

                    case Difficulty.HARD:
                        price = random.choice(itemDifficult)
                        question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le jeu coûte {price}€."
                        solution = []
                        left_to_pay=price
                        while (left_to_pay > 0):
                            i = 0
                            while (i<len(change) and change[i]>left_to_pay):
                                i += 1
                            left_to_pay -= change[i]
                            solution.add(change[i])
                return (question, str(solution))
            
            #acheter et payer deux objets
            case Category.TypeMM:
                match self.difficulty:
                    case Difficulty.EASY:
                       #vérifier la validité du prix, cad si la somme des deux appartient à la liste itemEasy
                       price_valid = False
                       while (price_valid == False) :
                        priceA = random.choice(itemEasy+itemDifficult)
                        priceB = random.choice(itemEasy+itemDifficult)
                        if (priceA+priceB) in itemEasy:
                            price = priceA+priceB
                            price_valid = True

                       question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le premier article coûte {priceA}€. Le deuxième article coûte {priceB}€."
                       solution = priceA+priceB                       

                    case Difficulty.HARD:
                        #vérifier la validité du prix, cad si la somme des deux appartient à la liste itemDifficult
                        price_valid = False
                        while (price_valid == False) :
                            priceA = random.choice(itemEasy+itemDifficult)
                            priceB = random.choice(itemEasy+itemDifficult)
                            if (priceA+priceB) in itemDifficult:
                                price = priceA+priceB
                                price_valid = True

                        solution = []
                        left_to_pay=price
                        i=len(change)-1
                        while (left_to_pay > 0 ):
                            if (left_to_pay-change[i])>=0:
                                left_to_pay=left_to_pay-change[i]
                                solution.add(change[i])
                            else :
                                i-=1
                return (question, str(solution)) 

            #vendre et rendre la monnaie d’un objet
            case Category.TypeR:
                match self.difficulty:
                    case Difficulty.EASY:
                        price = random.choice(itemEasy+itemDifficult)
                        change_valid = False
                        while (change_valid == False) :
                            nb_item_selct = random.choice([1, 2, 3])
                            change_client = random.sample(change, nb_item_selct)
                            #vérifier si le client a bien donné plus que le prix indiqué et si le retour de la monnaie est facile
                            if (sum(change_client)>=price) and (price-sum(change_client)in itemEasy) :
                                change_valid=True

                        question = f"Tu es le marchand, rends la monnaie au client.\nLe jeu coûte {price}€ et le client t'as donné {list(map(print, change_client))}."
                        solution = price-sum(change_client)
                
                    case Difficulty.HARD:
                        price = random.choice(itemEasy+itemDifficult)
                        change_valid = False
                        while (change_valid == False) :
                            nb_item_selct = random.choice([1, 2, 3])
                            change_client = random.sample(change, nb_item_selct)
                            #vérifier si le client a bien donné plus que le prix indiqué et si le retour de la monnaie est difficile
                            if (sum(change_client)>=price) and (price-sum(change_client)in itemDifficult) :
                                change_valid=True

                        question = f"Tu es le marchand, rends la monnaie au client.\nLe jeu coûte {price}€ et le client t'as donné {list(map(print, change_client))}."
                        solution = price-sum(change_client)
            
            #vendre et rendre la monnaie de deux objets
            case Category.TypeRM:              
                match self.difficulty:
                    case Difficulty.EASY:
                        priceA = random.choice(itemEasy+itemDifficult)
                        priceB = random.choice(itemEasy+itemDifficult)
                        change_valid = False
                        while (change_valid == False) :
                            nb_item_selct = random.choice([1, 2, 3])
                            change_client = random.sample(change, nb_item_selct)
                            if (sum(change_client)>=priceA+priceB) and (priceA+priceB-sum(change_client)in itemEasy) :
                                change_valid=True

                        question = f"Tu es le marchand, rends la monnaie au client. Le premier article coûte {priceA}€.\nLe deuxième article coûte {priceB}€. Le client t'as donné {list(map(print, change_client))}." 
                        solution = priceA+priceB-sum(change_client)
                
                    case Difficulty.HARD:
                        priceA = random.choice(itemEasy+itemDifficult)
                        priceB = random.choice(itemEasy+itemDifficult)
                        change_valid = False
                        while (change_valid == False) :
                            nb_item_selct = random.choice([1, 2, 3])
                            change_client = random.sample(change, nb_item_selct)
                            if (sum(change_client)>=priceA+priceB) and (priceA+priceB-sum(change_client)in itemDifficult) :
                                change_valid=True

                        question = f"Tu es le marchand, rends la monnaie au client. Le premier article coûte {priceA}€.\nLe deuxième article coûte {priceB}€. Le client t'as donné {list(map(print, change_client))}."
                        solution = priceA+priceB-sum(change_client)
        return question
    
    def get_distance(self, trial: dict) -> int:
        """
        parameters:
            - trial sous la forme {str(question), str(solution), str(answer)}
        return: la distance entre la solution et la réponse
        """
        distance = 0
        # TODO
        return distance
    
    def get_PDA(self, trial: dict) -> int:
        """
        calculer une mesure de la qualité de chaque activité, 
        mesurer combien de progrès a une activité prévue dans une fenêtre de temps récent.
        parameters:
            - Ck, k, t, d 
        return: la progression de l’apprentissage, r
        """
        r=0
        # TODO
        return r
    
    
    def try_question(self, question: dict) -> dict:
        """
        Let the user try a question, returns the trial and adds it to the self.previous_trials\n
        parameters:
            - question sous la forme {str(question), str(solution)}
            - 
        \n
        return: {str(question), str(solution), str(answer), str(distance)}
        """
        trial = dict(question)
        answer = ""
        
        # TODO

        trial['answer'] = answer
        trial['distance'] = self.get_distance(trial=trial)


        return trial

        
