from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import numpy as np

# Create your models here.
class Node(models.Model):

    class Category(models.TextChoices):
        TypeM = 'M'
        TypeMM = 'MM'
        TypeR = 'R'
        TypeRM = 'RM'
    class Difficulty(models.IntegerChoices):
        EASY = 0
        HARD = 1
        VERYHARD = 2
    class AnswerType(models.TextChoices):
        TEXT = 'T'
        LIST = 'L'
        INTEGER = 'I'

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=2, choices=Category, default=Category.TypeM)
    difficulty = models.IntegerField(choices=Difficulty, default=Difficulty.EASY)
    answer_type = models.CharField(max_length=1, choices=AnswerType, default=AnswerType.TEXT)
    default_quality = models.FloatField(default=0.0)
    default_probabilty = models.FloatField(default=0.0)

    def __str__(self):
        return f"Catégorie : {self.category} ; Difficulté : {self.difficulty}"

class Student(AbstractUser):

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    M_quality = models.FloatField(default=0.05)
    MM_quality = models.FloatField(default=0.05)
    R_quality = models.FloatField(default=0.0)
    RM_quality = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Exercice(models.Model):

    class State(models.TextChoices):
            DEACTIVATED = 'D', _('DEACTIVATED')
            ACTIVE = 'A', _('ACTIVE')
            UNEXPLORED = 'U',_('UNEXPLORED')

    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=2, choices=State, default=State.UNEXPLORED)
    node = models.ForeignKey(Node, on_delete=models.PROTECT, related_name='exercices')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercices')
    r_score = models.FloatField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    quality = models.FloatField(default=0.0)

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
    

################# SIGNALS #################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_exercises_for_student(sender, instance, created, **kwargs):
    if created:
        # Si un student est créé, on crée pour ce student autant d'exercices qu'il existe de nodes
        exercises = []
        for node in Node.objects.all():
            state = Exercice.State.UNEXPLORED
            if node.category == Node.Category.TypeM and node.difficulty == Node.Difficulty.EASY:
                state = Exercice.State.ACTIVE
            exercises.append(Exercice(student=instance, node=node, state=state))
        Exercice.objects.bulk_create(exercises)

@receiver(post_save, sender=Node)
def create_exercises_for_node(sender, instance, created, **kwargs):
    if created:
        # Si un node est créé, on crée pour chaque student un exercice
        exercises = []
        for student in Student.objects.all():
            exercises.append(Exercice(student=student, node=instance))
        Exercice.objects.bulk_create(exercises)