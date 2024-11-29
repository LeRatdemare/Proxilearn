from django.contrib import admin
from apppl.models import Node, Student, Exercice, Trial

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('category', 'difficulty')
    search_fields = ['name']

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')
    search_fields = ['name', 'surname']

class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('state', 'node', 'student', 'r_score')
    search_fields = ['state', 'node', 'student']

class TrialAdmin(admin.ModelAdmin):
    list_display = ('exercice', 'date', 'question', 'solution', 'student_answer', 'distance')
    search_fields = ['exercice', 'date', 'question', 'solution', 'student_answer']

admin.site.register(Node, NodeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(Trial, TrialAdmin)