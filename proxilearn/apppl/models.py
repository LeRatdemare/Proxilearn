from django.db import models
from django_enum import EnumField

# Create your models here.
class Node(models.Model):
    id = models.AutoField(primary_key=True)
    difficulty = models.IntegerField()
    category = models.IntegerField()
    
    def __str__(self):
        return f"Catégorie : {category} ; Difficulté : {difficulty}"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{name} {surname}"

class Exercice(models.Model):

    class State(models.TextChoices):
            SUCCEED = 'S', _('SUCCEED') 
            FAILED = 'F', _('FAILED')
            AVAILABLE = 'A', _('ACCESSIBLE')
            UNAVAILABLE = 'U',_('UNAVAILABLE')

    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=2, choices=State, default=State.UNAVAILABLE)
    node_id = models.IntegerField()
    student_id = models.IntegerField()
    r_score = models.IntegerField()

    def __str__(self):
        return self.name

class Trial(models.Model):
    id = models.AutoField(primary_key=True)
    exercice_id = models.IntegerField()
    date = models.models.DateField(_(""), auto_now=False, auto_now_add=False)
    question = models.TextField()
    solution = models.TextField()
    student_answer = models.TextField()
    distance = models.TextField()

    def __str__(self):
        return self.id