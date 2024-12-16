from apppl.models import Node, Student
from django.forms import ModelForm

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ('id', 'category', 'difficulty', 'answer_type')

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name')