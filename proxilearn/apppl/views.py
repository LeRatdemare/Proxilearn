from django.shortcuts import render, redirect
from apppl.models import Node
from apppl.forms import NodeForm, RegisterForm
from apppl.logic.code_ia import *

# Create your views here.
def index(request):
    user = request.user if request.user.is_authenticated else None
    
    exercices = Exercice.objects.filter(student=user) if user else None
    
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

        question = exercice_logic.generate_question()

        context = {
            'node': node,
            'student': student,
            'question': question,
            'user': user,
        }

        return render(request, 'exercice.html', context=context)
