from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Creamos una clase para decirle a la base de datos como va a almacenar datos

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) # Si no se pasa nada, el campo estara vacio
    created = models.DateTimeField(auto_now_add=True) # Creara la fecha actual, si no le pasamos este dato
    datecompleted = models.DateTimeField(null=True) # Campo vacio inicialmente
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Indicamos directamente con que otra tabla se va a relacionar, a traves de los id que se crean automaticamente en cada registro. Una Foreign Key es la clave que relaciona el valor de una tabla con el registro en otra, es lo que se usa en bases de datos relacionales
    def __str__(self):
        return self.title + " - by " + self.user.username