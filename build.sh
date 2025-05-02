#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
# Con este comando pip freeze > requirements.txt, se crea el archivo requirements.txt con todas las dependencias que necesita el proyecto. Al ejecutarlo con pip install, va a instalar todas las dependencias.
pip install -r requirements.txt # Importante ejecutar esto desde aqui para que luego cree las migraciones y no desde render.com

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate


# En render, crear una base de datos postgres y el internal URL agregarlo como una nueva variable de entorno llamada DATABASE_URL en el proyecto