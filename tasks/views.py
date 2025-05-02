from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import (
    UserCreationForm,
)  # Clase predefinida de Django para crear formularios
from django.contrib.auth.forms import (
    AuthenticationForm,
)  # Clase para comprobar si el usuario existe
from django.contrib.auth.models import User  # Clase para registrar usuarios
from django.contrib.auth import (
    logout,
    authenticate,
    login,
)  # Metodo para crear una cookie donde esten los datos de usuario y contraseña
from django.db import (
    IntegrityError,
)  # Para poder manejar los errores de integridad, por ejemplo si se quiere volver a crear un usuario ya creado
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # Decorador que permite proteger funciones, para limitar quienes pueden acceder a ellas

# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    # Cambiamos el render de acuerdo a si se viene a esta ruta con el metodo GET o POST
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        print(
            request.POST
        )  # Aca se puede ver los datos que envia el usuario en el formulario
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )  # Usamos el metodo para crear el usuario y le pasamos el nombre y contraseña.
                user.save()  # Se guarda en la base de datos
                login(
                    request, user
                )  # Con esta funcion se crea la cookie, para que se guarde la informacion del usuario que estamos autenticando
                return redirect("/tasks/")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm(), "error": "Username already exists"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm(), "error": "Passwords do not match"},
        )

@login_required # Es importante tener configurado en el archivo settings.py, donde esta el login para que se redirecciones alli
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # filtro para que se muestre las tareas que son del usuario que hace la peticion. datecompleted__isnull es una propiedad que se le crea a datecompleted y significa si datecompleted esta vacia o no al momento de crearse una tarea
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by("-datecompleted") # Se puede ordenar las tareas y se pasa el parametro con el que se ordena
    return render(request, "tasks.html", {
        "tasks": tasks
    })

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST) # Si el metodo al que se accede a esta url es POST, le pasamos los datos que el usuario introdujo en el formulario a traves de request.POST al TaskForm para que cree un formulario con esos datos
            new_task = form.save(commit=False) # Guardamos los datos del formulario, pero con commit=False, hacemos que no se guarde como una instancia de base de datos, sino que queremos que nos devuelva los datos que estan dentro de ese formulario
            new_task.user = request.user # En cada request que se envia, esta la informacion del usuario (dentro de las cookies, en la sesion que esta abierta)
            print(new_task)
            new_task.save() # Esto genera un dato dentro de la base de datos
            return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html", {
            "form": TaskForm,
            "error": "Please provide valid data"
        })

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Usamos el taskform para poder editar una tarea
        form = TaskForm(instance=task) # Se le pasa la tarea al parametro instance para que llene el formulario con esos datos
        return render(request, "task_detail.html", {
            "task":task,
            "form":form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user) # El usuario creador de la tarea tambien tiene que coincidir con el que hace la peticion para que no se puedan modificar tareas de otros usuarios
            # Se cambian los datos anteriores de la tarea por los actualizados
            form = TaskForm(request.POST, instance=task) # Se le pasan los datos de la request.POST y se le dice que es una instancia de task
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html", {
                "task":task,
                "form":form,
                "error": "Error updating task"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")

@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(
            request,
            "signin.html",
            {"form": AuthenticationForm},
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )  # Esto retorna un None si el user no es valido o un objeto User
        if user == None:
            return render(
                request,
                "signin.html",
                {"form": AuthenticationForm, "error": "Username or password is incorrect"},
            )
        else:
            login(request, user)
            return redirect("/tasks/")


