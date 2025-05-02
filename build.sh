#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
# Con este comando pip freeze > requirements.txt, se crea el archivo requirements.txt con todas las dependencias que necesita el proyecto. Al ejecutarlo con pip install, va a instalar todas las dependencias.
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate