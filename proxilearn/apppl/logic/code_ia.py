from django.conf import settings
from apppl.models import Node, Student, Exercice, Trial
import random
import numpy as np
from datetime import datetime

class ExerciceLogic:

    EXERCICES = [] # [ex1, ex2,...] on pourra appliquer prvious_trials
    FENETRE_D = 10
    OLD_REWARDS_IMPORTANCE = 0.5
    EXPLORATION_RATE = 0.1
    ZPD_EXERCISE_EXPANSION_THRESHOLD = 0.65
    ZPD_CATEGORY_EXPANSION_THRESHOLD = 0.50
    ACTIVITY_DEACTIVATING_THRESHOLD = 0.9
    MIN_NB_TRIALS_BEFORE_DEACTIVATING = 8
    DEFAULT_QUALITY = 0.2

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
        
        print(f"Preparing exercice for {student} of category {self.category} and difficulty {self.difficulty}")

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
            i = 0
            while i < len(change) and left_to_pay > 0:
                if left_to_pay - change[i] >= 0:
                    left_to_pay -= change[i]
                    solution.append(change[i])
                else:
                    i += 1  # Passe à une valeur plus petite si la valeur actuelle est trop grande
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
                        print(f"Price: {price}")
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
    
    def update_exercice_r_score(self) -> int:
        """
        Calculer une mesure du reward de chaque activité, 
        mesurer combien de progrès a une activité prévue dans une fenêtre de temps récent.
        parameters:
            - Ck, entre 0 et 1, si proche de 1, l’activité est réussie
            - k, le moment où on calcule la PDA
            - t, nombre total d’exercices effectués 
            - d, le nombre d’exercices retenus pour la comparaison
        return: la progression de l’apprentissage, r
        """
        r=0
        d = ExerciceLogic.FENETRE_D
        C=[]
        previous_trials = self.exercice.trials.all().order_by('datetime')
        print(f"Calculation of r_score for exercice {self.exercice} with {len(previous_trials)} previous trials")
        for i,trial in enumerate(previous_trials):
            distance = trial.distance
            C.append(1-distance)
            print(f"i={i} ; distance={distance} ; C[i]={C[i]}")
        t=len(previous_trials)

        for k in range(max(0,int(t-d/2)),t):
            r+=(C[k])/(d/2)
            print(f"r={r} ; k={k} ; C[k]={C[k]}")
        for k in range(max(0,t-d),min(1,int(t-d/2))):
            r-=(C[k])/(d/2)
            print(f"r={r} ; k={k} ; C[k]={C[k]}")
        
        self.exercice.r_score = r
        self.exercice.save()
        return r
    
    def update_category_r_score(self):
        """
        Update the r_score of the student for the category of the current exercice.
        """
        # We retrieve all the trials of the student for the category in active exercices
        trials = Trial.objects.filter(exercice__student=self.exercice.student, exercice__node__category=self.category, exercice__state=Exercice.State.ACTIVE).order_by('datetime')
        print(f"Calculation of r_score for category {self.category} with {len(trials)} previous trials")
        # We calculate the r_score for the category
        r_score = 0
        d = ExerciceLogic.FENETRE_D
        C = []
        for trial in trials:
            distance = trial.distance
            C.append(1-distance)
        t = len(trials)

        for k in range(max(0, int(t-d/2)), t):
            print(f"r_score={r_score} ; k={k} ; C[k]={C[k]}")
            r_score += (C[k]) / (d/2)
        for k in range(max(0, t-d), min(1, int(t-d/2))):
            r_score -= (C[k]) / (d/2)
            print(f"r_score={r_score} ; k={k} ; C[k]={C[k]}")
        
        # We update the r_score of the student for the category
        student: Student = self.exercice.student
        student.r_scores[self.category] = r_score
        student.save()
        return r_score

    def update_qualities(self):
        """
        Update the quality of the question type and the quality of the difficulty for this type.
        Requires the r_score of the exercice to be updated.
        """
        # We first update the category quality
        student: Student = self.exercice.student
        student.qualities[self.category] = ExerciceLogic.OLD_REWARDS_IMPORTANCE * student.qualities[self.category] + (1-ExerciceLogic.OLD_REWARDS_IMPORTANCE) * student.r_scores[self.category]
        student.save()
        # Then we update the exercice quality
        self.exercice.quality = ExerciceLogic.OLD_REWARDS_IMPORTANCE * self.exercice.quality + (1-ExerciceLogic.OLD_REWARDS_IMPORTANCE) * self.exercice.r_score
        self.exercice.save()
        return (student.qualities[self.category], self.exercice.quality)

    def update_current_exercice(self):
        """
        Update the current exercice of the student.
        Requires all the qualities of the student to be updated.
        """
        # Retrieve the student to get its category qualities
        student: Student = self.exercice.student

        # Sample a category using the qualities
        active_categories = [exercice.node.category for exercice in Exercice.objects.filter(student=student, state=Exercice.State.ACTIVE)]
        active_categories_qualities: dict = student.qualities
        # We only keep the qualities of the active categories
        active_categories_qualities = {category: quality for category, quality in active_categories_qualities.items() if category in active_categories}
        active_category_probabilities = dict()
        total_category_quality = sum(active_categories_qualities.values())

        for category, quality in active_categories_qualities.items():
            quality /= total_category_quality # Normalize the qualities
            active_category_probabilities[category] = quality * (1-ExerciceLogic.EXPLORATION_RATE) + ExerciceLogic.EXPLORATION_RATE * np.random.uniform(0, 1)
        # We normalize the probabilities
        total_probabilities = sum(active_category_probabilities.values())
        for category in active_category_probabilities:
            active_category_probabilities[category] /= total_probabilities
        # We sample a random category using the probabilities
        sampled_category = np.random.choice(list(active_category_probabilities.keys()), p=list(active_category_probabilities.values()))

        # Retrieve all the exercices of the student in the category
        exercices = Exercice.objects.filter(student=self.exercice.student, node__category=sampled_category, state=Exercice.State.ACTIVE)

        exercices_probabilities = dict()
        for exercice in exercices:
            normalized_quality = exercice.quality / sum([e.quality for e in exercices])
            exercices_probabilities[exercice] = normalized_quality * (1-ExerciceLogic.EXPLORATION_RATE) + ExerciceLogic.EXPLORATION_RATE * np.random.uniform(0, 1)
        # We normalize the probabilities
        total_probabilities = sum(exercices_probabilities.values())
        for exercice in exercices_probabilities:
            exercices_probabilities[exercice] /= total_probabilities
        # We sample a random exercice using the probabilities
        exercice: Exercice = np.random.choice(list(exercices_probabilities.keys()), p=list(exercices_probabilities.values()))
        # We set is_current to FALSE for every exercice of the student except the one we just sampled
        Exercice.objects.filter(student=self.exercice.student).update(is_current=False)

        exercice.is_current = True
        exercice.save()

        return exercice

    def update_zpd(self):
        """
        Update the ZPD of the student.
        """
        ### We first handle the ZPD expansion

        # For this, we get all the r_scores for the category and for all the active exercices
        student: Student = self.exercice.student
        category_r_scores = [exercice.r_score for exercice in Exercice.objects.filter(student=student, node__category=self.category, state=Exercice.State.ACTIVE)]
        all_active_student_r_scores = [exercice.r_score for exercice in Exercice.objects.filter(student=student, state=Exercice.State.ACTIVE)]

        ## We check if we have to add a new exercice in the same category
        print(f"Category r_scores: {category_r_scores}")
        mean_category_r_score = sum(category_r_scores) / len(category_r_scores)
        if mean_category_r_score >= ExerciceLogic.ZPD_EXERCISE_EXPANSION_THRESHOLD:
            # We update activate the next exercice in the same category
            next_exercice_same_category = Exercice.objects.filter(student=student, node__category=self.category, node__difficulty__gt=self.difficulty, state=Exercice.State.UNEXPLORED).order_by('node__difficulty').first()
            if next_exercice_same_category:
                next_exercice_same_category.state = Exercice.State.ACTIVE
                next_exercice_same_category.quality = ExerciceLogic.DEFAULT_QUALITY
                next_exercice_same_category.save()

        ## We check if we have to open a new category
        print(f"All active student r_scores: {all_active_student_r_scores}")
        mean_active_r_score = sum(all_active_student_r_scores) / len(all_active_student_r_scores)
        if mean_active_r_score >= ExerciceLogic.ZPD_CATEGORY_EXPANSION_THRESHOLD:
            # We randomly activate a new category among the ones that do not have active exercices
            categories: list = student.qualities.keys()
            active_categories = [exercice.node.category for exercice in Exercice.objects.filter(student=student, state=Exercice.State.ACTIVE)]
            inactive_categories = [category for category in categories if category not in active_categories]
            if inactive_categories:
                new_category = np.random.choice(inactive_categories)
                new_exercice = Exercice.objects.filter(student=student, node__category=new_category).order_by('node__difficulty').first()
                new_exercice.state = Exercice.State.ACTIVE
                new_exercice.quality = ExerciceLogic.DEFAULT_QUALITY
                new_exercice.save()

        ### Then we handle the deletion of the activities that are not in the ZPD anymore
        # We find the exercise that have the maximum r_score in the category
        max_r_score_exercice = Exercice.objects.filter(student=student, node__category=self.category, state=Exercice.State.ACTIVE).order_by('-r_score').first()
        # If its r_score is above the threshold
        if max_r_score_exercice.r_score > ExerciceLogic.ACTIVITY_DEACTIVATING_THRESHOLD and len(max_r_score_exercice.trials.all()) >= ExerciceLogic.MIN_NB_TRIALS_BEFORE_DEACTIVATING:
            # We deactivate the exercise and all the easier ones in the same category
            Exercice.objects.filter(student=student, node__category=self.category, node__difficulty__lte=max_r_score_exercice.node.difficulty).update(state=Exercice.State.DEACTIVATED)
  
    def _convert_attempt_to_valid_input(attempt: str, type: Node.AnswerType) -> str:
        """
        Convert the attempt to a valid input
        """
        if type == Node.AnswerType.LIST:
            l = attempt.split(",")
            for i in range(len(l)):
                l[i] = int(l[i])
            return str(l)
        
        return str(attempt)

    
    def try_question(self, question: dict, answer: str) -> dict:
        """
        Let the user try a question, returns the trial\n
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

        # On enregistre le trial dans la base de données
        Trial.objects.create(exercice=self.exercice, question=trial['question'], solution=trial['solution'], student_answer=trial['answer'], distance=trial['distance'])

        # On met à jour le r_score de l'exercice
        self.update_exercice_r_score()

        # On met à jour le r_score de la catégorie de l'exercice
        self.update_category_r_score()

        # On met à jour la qualité pour le type de l'exercice, ainsi que la qualité pour la difficulté correspondante
        self.update_qualities() # Besoin du r_score

        # On met à jour la ZPD de l'étudiant
        self.update_zpd() # Besoin du r_score (en vrai c'est SR=Success Rate mais on simplifie)

        # On met à jour les probabilités de chaque paramètre (category ET difficulty étant donné une category)
        # Puis on met à jour l'exercice courant en fonction
        self.update_current_exercice() # Besoin de la qualité

        return trial

        
