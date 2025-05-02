from django.contrib import admin
from .models import Task
# Register your models here.

# Para que el campo "created" de las tareas se vean en el panel de administrador, creamos una nueva clase
class TaskAdmin(admin.ModelAdmin): # Hereda todo lo del ModelAdmin
    readonly_fields = ("created",) # Se coloca una , al final porque es una tupla

# Hacer que la tabla Task tenga acceso al panel de administrador
admin.site.register(Task, TaskAdmin)