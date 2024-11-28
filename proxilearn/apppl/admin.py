from django.contrib import admin
from apppl.models import Node

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('category', 'difficulty')
    search_fields = ['name']

admin.site.register(Node, NodeAdmin)