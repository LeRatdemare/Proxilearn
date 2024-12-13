from apppl.models import Node, Student, Exercice, Trial
import random

class ExerciceLogic:

    EXERCICES = [] # [ex1, ex2,...] on pourra appliquer prvious_trials
    FENETRE_D=10 # à choisir ou il existe une valeur pertienente ?
    CHECK_THRESHOLD=0.7 # à choisir ou il existe une valeur pertienente ?
    FAIL_THRESHOLD=-0.8 # à choisir ou il existe une valeur pertienente ?
    
    def __init__(self, student, node):
        """
        parameters:
            - student : Student the student who is doing the exercice
            - node : Node the node of the exercice
        """
        try:
            self.exercice = Exercice.objects.get(node=node, student=student)
        except Exercice.DoesNotExist:
            self.exercice = Exercice.objects.create(node=node, student=student, state=Exercice.State.AVAILABLE)

        self.category: Node.Category = self.exercice.node.category
        self.difficulty: Node.Difficulty = self.exercice.node.difficulty
        print(f"Preparing exercice for {student} of category {self.category} and difficulty {self.difficulty}")
        self.previous_trials: list[dict[str, str, str, float]] = [] # [{question, solution, answer, distance}, ...]
        
        for trial in self.exercice.trials.all():
            self.previous_trials.append({
                'question': trial.question,
                'solution': trial.solution,
                'answer': trial.student_answer,
                'distance': trial.distance
            })

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
            case Node.Category.TypeM:
                match self.difficulty:
                    case Node.Difficulty.EASY:
                       price = random.choice(itemEasy)
                       question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le jeu coûte {price}€."
                       solution = price                      

                    case Node.Difficulty.HARD:
                        price = random.choice(itemDifficult)
                        question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le jeu coûte {price}€."
                        solution = []
                        left_to_pay=price
                        while (left_to_pay > 0):
                            i = 0
                            while (i<len(change) and change[i]>left_to_pay):
                                i += 1
                            left_to_pay -= change[i]
                            solution.append(change[i])
            
            #acheter et payer deux objets
            case Node.Category.TypeMM:
                match self.difficulty:
                    case Node.Difficulty.EASY:
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

                    case Node.Difficulty.HARD:
                        #vérifier la validité du prix, cad si la somme des deux appartient à la liste itemDifficult
                        price_valid = False
                        while (price_valid == False) :
                            priceA = random.choice(itemEasy+itemDifficult)
                            priceB = random.choice(itemEasy+itemDifficult)
                            if (priceA+priceB) in itemDifficult:
                                price = priceA+priceB
                                price_valid = True

                        question = f"Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. Le premier article coûte {priceA}€. Le deuxième article coûte {priceB}€."
                        solution = []
                        left_to_pay=price
                        i=len(change)-1
                        while (left_to_pay > 0 ):
                            if (left_to_pay-change[i])>=0:
                                left_to_pay=left_to_pay-change[i]
                                solution.append(change[i])
                            else :
                                i-=1

            #vendre et rendre la monnaie d’un objet
            case Node.Category.TypeR:
                match self.difficulty:
                    case Node.Difficulty.EASY:
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
                
                    case Node.Difficulty.HARD:
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
            case Node.Category.TypeRM:              
                match self.difficulty:
                    case Node.Difficulty.EASY:
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
                
                    case Node.Difficulty.HARD:
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

        return {'question':question, 'solution':solution}
    
    def get_distance(trial: dict) -> int:
        """
        parameters:
            - trial sous la forme {str(question), str(solution), str(answer)}
        return: la distance entre la solution et la réponse
        """
        if (trial['solution']==trial['answer']):
            return 0
        return 1
    
    def update_r_score(self, d:int = FENETRE_D) -> int:
        """
        calculer une mesure de la qualité de chaque activité, 
        mesurer combien de progrès a une activité prévue dans une fenêtre de temps récent.
        parameters:
            - Ck, 
            - k, le moment où on calcule la PDA
            - t, nombre total d’exercices effectués 
            - d, le nombre d’exercices retenus pour la comparaison
        return: la progression de l’apprentissage, r
        """
        r=0
        
        C=[]
        for trial in self.previous_trials:
            distance = trial['distance']
            C.append(1-distance)
        t=len(self.previous_trials)

        for k in range(max(0,int(t-d/2)),t):
            print(f"Bonus part ===> t={t}, k={k}, d={d}")
            r+=(C[k])/(d/2)
        for k in range(max(0,t-d),min(1,int(t-d/2))):
            print(f"Malus part ===> t={t}, k={k}, d={d}")
            r-=(C[k])/(d/2)
        
        self.exercice.r_score = r
        self.exercice.save()

        return r
    
    def update_exercices(self):
        """
        Update the neighbors' states of the current exercice
        according to its r_score.
        """
        # Check if the exercice should be SUCCEED, FAILED or stay AVAILABLE
        if self.exercice.r_score >= ExerciceLogic.CHECK_THRESHOLD:
            self.exercice.state = Exercice.State.SUCCEED
        elif self.exercice.r_score <= ExerciceLogic.FAIL_THRESHOLD:
            self.exercice.state = Exercice.State.FAILED
        self.exercice.save()

        if self.exercice.state == Exercice.State.SUCCEED:
            # We first get the next UNAVAILABLE Exercice in same category to make it AVAILABLE
            next_exercice_same_category = Exercice.objects.filter(student=self.exercice.student, node__category=self.category, node__difficulty__gt=self.difficulty, state=Exercice.State.UNAVAILABLE).order_by('-node__difficulty').first()
            if next_exercice_same_category:
                next_exercice_same_category.state = Exercice.State.AVAILABLE
                next_exercice_same_category.save()
            
        elif self.exercice.state == Exercice.State.FAILED:
            # We find the previous exercice in the same category to make it AVAILABLE
            previous_exercice_same_category = Exercice.objects.filter(student=self.exercice.student, node__category=self.category, node__difficulty__lt=self.difficulty, state=Exercice.State.SUCCEED).order_by('node__difficulty').first()
            if previous_exercice_same_category:
                previous_exercice_same_category.state = Exercice.State.AVAILABLE
                previous_exercice_same_category.save()
        
        # In both cases we make another exercice of the same difficulty AVAILABLE 
        if self.exercice.state == Exercice.State.SUCCEED or self.exercice.state == Exercice.State.FAILED:
            other_exercices_same_difficulty = Exercice.objects.filter(student=self.exercice.student, node__difficulty=self.difficulty, state=Exercice.State.UNAVAILABLE).exclude(node__category=self.category)
            if other_exercices_same_difficulty:
                # We choose a random exercice
                next_exercice_same_difficulty = random.choice(other_exercices_same_difficulty)
                next_exercice_same_difficulty.state = Exercice.State.AVAILABLE
                next_exercice_same_difficulty.save()
            
        # TODO : Make sure that there is always at least 2 exercices AVAILABLE
    
    def _convert_attempt_to_valid_input(attempt: str) -> str:
        """
        Convert the attempt to a valid input
        """
        l = attempt.split(",")
        for i in range(len(l)):
            l[i] = int(l[i])
        print(f"Attemp {attempt} to list ===> {l}")
        return str(l)
    
    def try_question(self, question: dict, answer: str) -> dict:
        """
        Let the user try a question, returns the trial and adds it to the self.previous_trials\n
        parameters:
            - question sous la forme {str(question), str(solution)}
            - answer sous la forme str(answer)
        \n
        return: {str(question), str(solution), str(answer), str(distance)}
        """
        if self.exercice.state != Exercice.State.AVAILABLE:
            raise Exception("Exercice is not available")
        
        trial = dict(question)
        trial['answer'] = ExerciceLogic._convert_attempt_to_valid_input(answer)
        trial['distance'] = ExerciceLogic.get_distance(trial) # WARNING this line is tricky and cause problems
        print(f"Trial: {trial}")

        # On enregistre le trial dans la base de données
        Trial.objects.create(exercice=self.exercice, question=trial['question'], solution=trial['solution'], student_answer=trial['answer'], distance=trial['distance'])
        self.previous_trials.append(trial)

        # On met à jour le r_score de l'exercice
        self.update_r_score()

        # On met à jour les exercices
        self.update_exercices()

        return trial

        
