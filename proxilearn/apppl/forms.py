from apppl.models import Exercice
from django.forms import ModelForm

class ExerciceForm(ModelForm):
    class Meta:
        model = Exercice
        fields = ('name', 'description', 'difficulty', 'category')