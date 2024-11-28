from django.shortcuts import render
from apppl.models import Node
from apppl.forms import NodeForm
from apppl.logic.code_ia import *

# Create your views here.
def index(request):
    formulaire = NodeForm()

    if request.method == 'POST':
        formulaire = NodeForm(request.POST)
        if formulaire.is_valid():
            formulaire.save()
        else:
            print(formulaire.errors)
    
    context = {
        'exercices': Node.objects.all(),
        'formulaire': formulaire
    }
    learning = True
    while learning == True :
        learning = False

    return render(request, 'index.html', context)