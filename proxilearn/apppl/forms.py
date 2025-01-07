from apppl.models import Node
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ('id', 'category', 'difficulty', 'answer_type', 'default_quality')