from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apppl.models import Node, Student, Exercice, Trial

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'difficulty', 'answer_type', 'default_quality')
    search_fields = ['name']

class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'node', 'student', 'trial_count','r_score', 'quality', 'is_current')
    search_fields = ['state', 'node', 'student']

class TrialAdmin(admin.ModelAdmin):
    list_display = ('id', 'exercice', 'datetime', 'question', 'solution', 'student_answer', 'distance')
    search_fields = ['exercice', 'datetime', 'question', 'solution', 'student_answer']

class StudentUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'r_scores', 'qualities')
    search_fields = ['username', 'first_name', 'last_name']

admin.site.register(Node, NodeAdmin)
admin.site.register(Student, StudentUserAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(Trial, TrialAdmin)