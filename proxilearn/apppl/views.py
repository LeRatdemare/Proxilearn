from django.shortcuts import render
from apppl.models import Exercice
from apppl.forms import ExerciceForm
from apppl.logic.code_ia import *

# Create your views here.
def index(request):
    formulaire = ExerciceForm()

    if request.method == 'POST':
        formulaire = ExerciceForm(request.POST)
        if formulaire.is_valid():
            formulaire.save()
        else:
            print(formulaire.errors)
    
    context = {
        'exercices': Exercice.objects.all(),
        'formulaire': formulaire
    }
    return render(request, 'index.html', context)