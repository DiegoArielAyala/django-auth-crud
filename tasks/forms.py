from django import (
    forms,
)  # Es una clase que podemos extender para crear nuestros propios formularios
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        # Indicamos en que modelo (desde models.py) va a estar basado el formulario
        model = Task
        fields = [
            "title",
            "description",
            "important",
        ]  # Le paso los campos que quiero en el formulario

        # Widgets permite colocar un diccionario comun como valor para añadir clases. Sirve para asignar otros atributos a los inputs "fields" que esta generando
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Write a title"}
            ),  # Se pasan los atributos en forma de diccionario, "class" es del html y "form-control" es la sintaxis de bootstrap
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Write a description"}
            ),
            "important": forms.CheckboxInput(
                attrs={"class": "form-check-input m-auto"}
            ),
        }
