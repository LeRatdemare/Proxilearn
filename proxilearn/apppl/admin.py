from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apppl.models import Node, Student, Exercice, Trial

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'difficulty', 'answer_type')
    search_fields = ['name']

class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'node', 'student', 'r_score')
    search_fields = ['state', 'node', 'student']

class TrialAdmin(admin.ModelAdmin):
    list_display = ('id', 'exercice', 'date', 'question', 'solution', 'student_answer', 'distance')
    search_fields = ['exercice', 'date', 'question', 'solution', 'student_answer']

admin.site.register(Node, NodeAdmin)
admin.site.register(Student, UserAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(Trial, TrialAdmin)