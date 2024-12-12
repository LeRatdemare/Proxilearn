from django.shortcuts import render
from apppl.models import Node
from apppl.forms import NodeForm, StudentForm
from apppl.logic.code_ia import *

# Create your views here.
def index(request):
    formulaire_node = NodeForm()
    formulaire_student = StudentForm()

    if request.method == 'POST':
        # On vérifie si c'est un formulaire de node ou de student
        if 'student' in request.POST:
            formulaire_student = StudentForm(request.POST)
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
        'students': Student.objects.all(),
        'formulaire_node': formulaire_node,
        'formulaire_student': formulaire_student,
    }
    learning = True
    while learning == True :
        learning = False

    return render(request, 'index.html', context)

def exercice(request, node_id, student_id):
        print(f"Exercice {node_id} pour l'étudiant {student_id}")
        node = Node.objects.get(pk=node_id)
        student = Student.objects.get(pk=student_id)

        exercice_logic = ExerciceLogic(student=student, node=node)

        context = {
            
        }

        return render(request, 'exercice.html', context=context)
