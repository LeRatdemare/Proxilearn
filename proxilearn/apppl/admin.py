from django.contrib import admin
from apppl.models import Exercice

# Register your models here.

class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'category')
    search_fields = ['name']

admin.site.register(Exercice, ExerciceAdmin)