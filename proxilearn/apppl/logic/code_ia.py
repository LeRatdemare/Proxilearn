from category import Category
from difficulty import Difficulty

class Exercice:

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

        match self.category:
            case Category.A:
                match self.difficulty:
                    case Difficulty.EASY:
                        ... # TODO
                    case Difficulty.MEDIUM:
                        ... # TODO
                    case Difficulty.HARD:
                        ... # TODO
            case Category.B:
                match self.difficulty:
                    case Difficulty.EASY:
                        ... # TODO
                    case Difficulty.MEDIUM:
                        ... # TODO
                    case Difficulty.HARD:
                        ... # TODO
        
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

        
