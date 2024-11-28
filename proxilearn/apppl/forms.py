from apppl.models import Node
from django.forms import ModelForm

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ('id', 'category', 'difficulty')