from django.db import models

# Create your models here.
class Exercice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.IntegerField()
    category = models.IntegerField()