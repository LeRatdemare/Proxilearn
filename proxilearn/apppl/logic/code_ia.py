from django.conf import settings
from apppl.models import Node, Student, Exercice, Trial
import random
import numpy as np

class ExerciceLogic:

    EXERCICES = [] # [ex1, ex2,...] on pourra appliquer prvious_trials
    FENETRE_D = 10
    OLD_REWARDS_IMPORTANCE = 0.5
    EXPLORATION_RATE = 0.1
    ZPD_EXPANSION_THRESHOLD = 0.5
    ACTIVITY_DEACTIVATING_THRESHOLD = 0.7

    # @classmethod
    # def load_constants(cls):
    #     constants_file = os.path.join(settings.BASE_DIR, 'data', 'constantes.json')
    #     with open(constants_file, 'r') as file:
    #         constants = json.load(file)

    #     cls.FENETRE_D = constants.get('FENETRE_D', 10)
    #     cls.OLD_REWARDS_IMPORTANCE = constants.get('OLD_REWARDS_IMPORTANCE', 0.5)
    #     cls.EXPLORATION_RATE = constants.get('EXPLORATION_RATE', 0.1)
    #     cls.ZPD_EXPANSION_THRESHOLD = constants.get('ZPD_EXPANSION_THRESHOLD', 0.5)
    #     cls.ACTIVITY_DEACTIVATING_THRESHOLD = constants.get('ACTIVITY_DEACTIVATING_THRESHOLD', 0.7)

    # load_constants()

    def __init__(self, student, node):
        """
        parameters:
            - student : Student the student who is doing the exercice
            - node : Node the node of the exercice
        """
        try:
            self.exercice = Exercice.objects.get(node=node, student=student)
        except Exercice.DoesNotExist:
            self.exercice = Exercice.objects.create(node=node, student=student, state=Exercice.State.ACTIVE)

        self.category: Node.Category = self.exercice.node.category
        self.difficulty: Node.Difficulty = self.exercice.node.difficulty
        
        self.quality: float = self.exercice.quality

        match self.category:
            case Node.Category.TypeM:
                self.category_quality = student.M_quality
            case Node.Category.TypeMM:
                self.category_quality = student.MM_quality
            case Node.Category.TypeR:
                self.category_quality = student.R_quality
            case Node.Category.TypeRM:
                self.category_quality = student.RM_quality
        
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

        return: question sous la forme {str(question), str(solution), str(answer_type)}
        """
        question = {"question": str(), "solution": str(), "answer_type": str()}
        change = [10,5,2,1,0.5,0.2,0.1] #pièces et billets disponibles
        itemEasy = [1,2,5,10] #à lecture directe, c’est-à-dire si une pièce ou un billet de la valeur de ce montant existe
        itemDifficult = [3,4,6,7,8,9,11,12,13,14,15,16,17,18,19] #combiner plusieurs monnaie
        itemVeryDifficult = [] #combiner une pièce ou un billet avec une pièce de centime
        for item in itemEasy :
            for i in range (4):
                itemVeryDifficult.append(item+change[i])

        def calculate_solution(price, change):
            # Calcule la solution en décomposant le prix avec les valeurs disponibles dans change.
            solution = []
            left_to_pay = price
            i = len(change) - 1  # Commence par la plus grande valeur de "change"
            while left_to_pay > 0:
                if left_to_pay - change[i] >= 0:
                    left_to_pay -= change[i]
                    solution.append(change[i])
                else:
                    i -= 1  # Passe à une valeur plus petite si la valeur actuelle est trop grande
            return solution

        match self.category:
            #acheter et payer un objet
            case Node.Category.TypeM:
                match self.difficulty:
                    case Node.Difficulty.EASY:
                       price = random.choice(itemEasy)
                       solution = price
                       answer_type = Node.AnswerType.INTEGER

                    case Node.Difficulty.HARD:
                        price = random.choice(itemDifficult)
                        answer_type = Node.AnswerType.LIST
                        solution = calculate_solution(price, change)

                    case Node.Difficulty.VERYHARD:
                        price = random.choice(itemVeryDifficult)
                        answer_type = Node.AnswerType.LIST
                        solution = calculate_solution(price, change)
                        
                question = f"""Tu es le client, paie ce que tu dois au marchand avec 
                les pièces et les billets. Le jeu coûte {price}€."""
            
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
                        solution = priceA+priceB
                        answer_type = Node.AnswerType.INTEGER

                    case Node.Difficulty.HARD:
                        #vérifier la validité du prix, cad si la somme des deux appartient à la liste itemDifficult
                        price_valid = False
                        while (price_valid == False) :
                            priceA = random.choice(itemEasy+itemDifficult)
                            priceB = random.choice(itemEasy+itemDifficult)
                            if (priceA+priceB) in itemDifficult:
                                price = priceA+priceB
                                price_valid = True

                        solution = calculate_solution(price, change)

                    
                    case Node.Difficulty.VERYHARD:
                        price_valid = False
                        while (price_valid == False) :
                            priceA = random.choice(itemVeryDifficult)
                            priceB = random.choice(change[:,3])

                        solution = calculate_solution(price, change)


                question = f"""Tu es le client, paie ce que tu dois au marchand avec les pièces et les billets. 
                Le premier article coûte {priceA}€. Le deuxième article coûte {priceB}€."""

            #vendre et rendre la monnaie d’un objet
            case Node.Category.TypeR:
                def generate_question_typeR(price, change, valid_items, answer_type):
                    #Génère une question et une solution pour rendre la monnaie.
                    change_valid = False
                    while not change_valid:
                        nb_item_select = random.choice([1, 2, 3])
                        change_client = random.sample(change, nb_item_select)
                        # Vérifier si le client a donné plus que le prix et si le rendu est valide
                        if sum(change_client) >= price and (sum(change_client) - price) in valid_items:
                            change_valid = True

                    question = (
                        f"""Tu es le marchand, rends la monnaie au client.\n
                        Le jeu coûte {price}€ et le client t'a donné {list(map(str, change_client))}."""
                    )
                    solution = sum(change_client) - price
                    return question, solution, answer_type

                price = random.choice(itemEasy + itemDifficult)
                
                # Dans le match statement
                match self.difficulty:
                    case Node.Difficulty.EASY:
                        question, solution, answer_type = generate_question_typeR(
                            price, change, itemEasy, Node.AnswerType.INTEGER
                        )

                    case Node.Difficulty.HARD:
                        question, solution, answer_type = generate_question_typeR(
                            price, change, itemDifficult, Node.AnswerType.LIST
                        )
                    
                    case Node.Difficulty.VERYHARD:
                            question, solution, answer_type = generate_question_typeR(
                                price, change, itemVeryDifficult, Node.AnswerType.LIST
                            )

            
            #vendre et rendre la monnaie de deux objets
            case Node.Category.TypeRM:              
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

                # Dans le match statement
                match self.difficulty:
                    case Node.Difficulty.EASY:
                        priceA = random.choice(itemEasy + itemDifficult)
                        priceB = random.choice(itemEasy + itemDifficult)
                        question, solution, answer_type = generate_multi_item_change_question(
                            priceA, priceB, change, itemEasy, Node.AnswerType.INTEGER
                        )

                    case Node.Difficulty.HARD:
                        priceA = random.choice(itemEasy + itemDifficult)
                        priceB = random.choice(itemEasy + itemDifficult)
                        question, solution, answer_type = generate_multi_item_change_question(
                            priceA, priceB, change, itemDifficult, Node.AnswerType.LIST
                        )

                    case Node.Difficulty.VERYHARD:
                        priceA = random.choice(itemEasy + itemDifficult)
                        priceB = random.choice(itemEasy + itemDifficult)
                        question, solution, answer_type = generate_multi_item_change_question(
                            priceA, priceB, change, itemVeryDifficult, Node.AnswerType.LIST
                        )


        return {'question':question, 'solution':solution, 'answer_type':answer_type}
    
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
    
    def update_qualities(self):
        """
        Update the quality of the question type and the quality of the difficulty for this type.
        """
        # We first update the category quality

        # Then we update the exercice quality
        pass

    def update_current_exercice(self):
        """
        Update the current exercice of the student.
        Requires all the qualities of the student to be updated.
        """
        # Retrieve the student to get its category qualities
        student = self.exercice.student

        # Sample a category using the qualities
        category_qualities = {
            Node.Category.TypeM: student.M_quality,
            Node.Category.TypeMM: student.MM_quality,
            Node.Category.TypeR: student.R_quality,
            Node.Category.TypeRM: student.RM_quality
        }
        category_probabilities = dict()
        for category, quality in category_qualities.items():
            quality = quality / sum(category_qualities.values()) # Normalize the qualities
            category_probabilities[category] = quality * (1-ExerciceLogic.EXPLORATION_RATE) + ExerciceLogic.EXPLORATION_RATE * np.random.uniform(0, 1)
        # We sample a random category using the probabilities
        category = np.random.choice(list(category_probabilities.keys()), p=list(category_probabilities.values()))

        # Retrieve all the exercices of the student in the category
        exercices = Exercice.objects.filter(student=self.exercice.student, node__category=category)

        exercices_probabilities = dict()
        for exercice in exercices:
            normalized_quality = exercice.quality / sum([e.quality for e in exercices])
            exercices_probabilities[exercice] = normalized_quality * (1-ExerciceLogic.EXPLORATION_RATE) + ExerciceLogic.EXPLORATION_RATE * np.random.uniform(0, 1)
        # We sample a random exercice using the probabilities
        exercice: Exercice = np.random.choice(list(exercices_probabilities.keys()), p=list(exercices_probabilities.values()))
        exercice.is_current = True
        # We set is_current to FALSE for every exercice of the student except the one we just sampled
        Exercice.objects.filter(student=self.exercice.student).exclude(node=exercice.node).update(is_current=False)

        exercice.save()

    def update_zpd(self):
        """
        Update the ZPD of the student.
        """
        # We first check if the global
        pass

    def set_current_exercice(self):
        """
        Among all the exercices available, choose the one with the highest probability and set it as the current exercice
        """
        pass

    # def update_exercices(self):
    #     """
    #     Update the neighbors' states of the current exercice
    #     according to its r_score.
    #     """
    #     # Check if the exercice should be SUCCEED, FAILED or stay AVAILABLE
    #     if self.exercice.r_score >= ExerciceLogic.CHECK_THRESHOLD:
    #         self.exercice.state = Exercice.State.DEACTIVATED
    #     elif self.exercice.r_score <= ExerciceLogic.FAIL_THRESHOLD:
    #         self.exercice.state = Exercice.State.FAILED
    #     self.exercice.save()

    #     if self.exercice.state == Exercice.State.DEACTIVATED:
    #         # We first get the next UNAVAILABLE Exercice in same category to make it AVAILABLE
    #         next_exercice_same_category = Exercice.objects.filter(student=self.exercice.student, node__category=self.category, node__difficulty__gt=self.difficulty).exclude(state=Exercice.State.ACTIVE).order_by('-node__difficulty').first()
    #         if next_exercice_same_category:
    #             next_exercice_same_category.state = Exercice.State.ACTIVE
    #             next_exercice_same_category.save()
            
    #     elif self.exercice.state == Exercice.State.FAILED:
    #         # We find the previous exercice in the same category to make it AVAILABLE
    #         previous_exercice_same_category = Exercice.objects.filter(student=self.exercice.student, node__category=self.category, node__difficulty__lt=self.difficulty).exclude(state=Exercice.State.ACTIVE).order_by('node__difficulty').first()
    #         if previous_exercice_same_category:
    #             previous_exercice_same_category.state = Exercice.State.ACTIVE
    #             previous_exercice_same_category.save()
        
    #     # In both cases we make another exercice of the same difficulty AVAILABLE 
    #     if self.exercice.state == Exercice.State.DEACTIVATED or self.exercice.state == Exercice.State.FAILED:
    #         other_exercices_same_difficulty = Exercice.objects.filter(student=self.exercice.student, node__difficulty=self.difficulty).exclude(node__category=self.category, state=Exercice.State.ACTIVE)
    #         if other_exercices_same_difficulty:
    #             # We choose a random exercice
    #             next_exercice_same_difficulty = random.choice(other_exercices_same_difficulty)
    #             next_exercice_same_difficulty.state = Exercice.State.ACTIVE
    #             next_exercice_same_difficulty.save()
            
    #     # TODO : Make sure that there is always at least 2 exercices AVAILABLE
    
    def _convert_attempt_to_valid_input(attempt: str, type: Node.AnswerType) -> str:
        """
        Convert the attempt to a valid input
        """
        if type == Node.AnswerType.LIST:
            l = attempt.split(",")
            for i in range(len(l)):
                l[i] = int(l[i])
            print(f"Attemp {attempt} to list ===> {l}")
            return str(l)
        
        return str(attempt)

    
    def try_question(self, question: dict, answer: str) -> dict:
        """
        Let the user try a question, returns the trial and adds it to the self.previous_trials\n
        parameters:
            - question sous la forme {str(question), str(solution), str(answer_type)}
            - answer sous la forme str(answer)
        \n
        return: {str(question), str(solution), str(answer), str(answer_type), str(distance)}
        """
        if self.exercice.state != Exercice.State.ACTIVE:
            raise Exception("Exercice is not available")
        
        trial = dict(question)
        trial['answer'] = ExerciceLogic._convert_attempt_to_valid_input(answer, question['answer_type'])
        trial['distance'] = ExerciceLogic.get_distance(trial) # WARNING this line is tricky and cause problems
        print(f"Trial: {trial}")

        # On enregistre le trial dans la base de données
        Trial.objects.create(exercice=self.exercice, question=trial['question'], solution=trial['solution'], student_answer=trial['answer'], distance=trial['distance'])
        self.previous_trials.append(trial)

        # On met à jour le r_score de l'exercice
        self.update_r_score()

        # On met à jour la qualité pour le type de l'exercice, ainsi que la qualité pour la difficulté correspondante
        self.update_qualities() # Besoin du r_score

        # On met à jour les probabilités de chaque paramètre (category ET difficulty étant donné une category)
        self.update_current_exercice() # Besoin de la qualité

        # On met à jour la ZPD de l'étudiant
        self.update_zpd() # Besoin du r_score (en vrai c'est SR=Success Rate mais on simplifie)

        # On sélectionne un nouvel exercice pour l'étudiant
        self.set_current_exercice() # Besoin de la proba

        return trial

        
