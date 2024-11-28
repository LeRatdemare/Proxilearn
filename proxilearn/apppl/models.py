from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Node(models.Model):

    class Category(models.TextChoices):
        TypeM = 'M'
        TypeMM = 'MM'
        TypeR = 'R'
        TypeRM = 'RR'
    class Difficulty(models.IntegerChoices):
        EASY = 0
        HARD = 1

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=2, choices=Category, default=Category.TypeM)
    difficulty = models.IntegerField(choices=Difficulty, default=Difficulty.EASY)
    
    def __str__(self):
        return f"Catégorie : {self.category} ; Difficulté : {self.difficulty}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Exercice(models.Model):

    class State(models.TextChoices):
            SUCCEED = 'S', _('SUCCEED') 
            FAILED = 'F', _('FAILED')
            AVAILABLE = 'A', _('AVAILABLE')
            UNAVAILABLE = 'U',_('UNAVAILABLE')

    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=2, choices=State, default=State.UNAVAILABLE)
    node = models.ForeignKey(Node, on_delete=models.PROTECT, blank=False, null=False, related_name='exercices')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False, related_name='exercices')
    r_score = models.FloatField()

    def __str__(self):
        return f"Exo{self.id} ==> {self.state}"

class Trial(models.Model):
    id = models.AutoField(primary_key=True)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, blank=False, null=False, related_name='trials')
    date = models.DateField(auto_now=False, auto_now_add=True)
    question = models.CharField(max_length=255, blank=False, null=False)
    solution = models.CharField(max_length=255, blank=False, null=False)
    student_answer = models.CharField(max_length=255, blank=False, null=False)
    distance = models.FloatField()

    def __str__(self):
        return f"{self.question} ; distance={self.distance}"