from django.shortcuts import render, redirect
from apppl.models import Node, Student, Exercice, Trial
from apppl.models import generate_default_qualities, generate_default_r_scores
from apppl.forms import NodeForm, RegisterForm
from apppl.logic.code_ia import *

# Create your views here.
def index(request):
    user = request.user if request.user.is_authenticated else None
    
    exercices = Exercice.objects.filter(student=user) if user else None
    current_exercice = Exercice.objects.filter(student=user, is_current=True).first() if user else None

    formulaire_node = NodeForm()
    formulaire_student = RegisterForm()

    if request.method == 'POST':
        # On vérifie si c'est un formulaire de node ou de student
        if 'student' in request.POST:
            formulaire_student = RegisterForm(request.POST)
            if formulaire_student.is_valid():
                formulaire_student.save()
            else:
                print(formulaire_student.errors)
        else:
            formulaire_node = NodeForm(request.POST)
            if formulaire_node.is_valid():
                formulaire_node.save()
            else:
                print(formulaire_node.errors)
    
    context = {
        'nodes': Node.objects.all(),
        'exercices': exercices,
        'current_exercice': current_exercice,
        'students': Student.objects.all(),
        'formulaire_node': formulaire_node,
        'formulaire_student': formulaire_student,
        'user': user,
    }

    learning = True
    while learning == True :
        learning = False

    return render(request, 'index.html', context)

def exercice(request, student_id):
        user = request.user if request.user.is_authenticated else None

        student = Student.objects.get(pk=student_id)
        exercice = Exercice.objects.get(student=student, is_current=True)
        node = Node.objects.get(pk=exercice.node_id)
        
        # Si l'exercice n'est pas disponible, on redirige vers l'accueil
        if exercice.state != Exercice.State.ACTIVE:
            return redirect('index')

        exercice_logic = ExerciceLogic(node=node, student=student)

        if request.method == 'POST':
            # On récupère la question et la réponse de l'étudiant
            question = {'question':request.POST.get('question'), 'solution':request.POST.get('solution'), 'answer_type':request.POST.get('answer_type')}
            student_answer = request.POST.get('student_answer')
            # On crée un essai
            trial = exercice_logic.try_question(question, student_answer)
            print(f"Essai: {trial}")

            ## On sélectionne le prochain exercice qui a peut-être changé
            exercice = Exercice.objects.get(student=student, is_current=True)
            node = Node.objects.get(pk=exercice.node_id)
            if exercice.state != Exercice.State.ACTIVE:
                return redirect('index')
            exercice_logic = ExerciceLogic(node=node, student=student)

        # On génère une nouvelle question
        question = exercice_logic.generate_question()
        context = {
            'node': node,
            'student': student,
            'question': question,
            'user': user,
        }
        return render(request, 'exercice.html', context=context)

def reset_all(request):
    if request.method == 'POST' and request.user.is_superuser:
        # We delete all the trials, exercices and nodes
        Trial.objects.all().delete()
        Exercice.objects.all().delete()
        Node.objects.all().delete()

        # We recreate one node for each category and difficulty
        for category in Node.Category:
            for difficulty in Node.Difficulty:
                match difficulty:
                    case Node.Difficulty.EASY:
                        answer_type = Node.AnswerType.INTEGER
                    case Node.Difficulty.HARD:
                        answer_type = Node.AnswerType.LIST
                    case Node.Difficulty.VERYHARD:
                        answer_type = Node.AnswerType.LIST
                node = Node.objects.create(category=category, difficulty=difficulty, answer_type=answer_type)
                # We create one exercice per Node for each student
                i = 0
                for student in Student.objects.all():
                    print(f"[{i}] Création de l'exercice pour {student}")
                    Exercice.objects.create(node=node, student=student)
        # We set the current exercice for each student
        Exercice.objects.filter(node__category=Node.Category.TypeM, node__difficulty=Node.Difficulty.EASY).update(is_current=True, state=Exercice.State.ACTIVE)
        Student.objects.update(r_scores=generate_default_r_scores(), qualities=generate_default_qualities())
        return redirect('index')
    return redirect('index')