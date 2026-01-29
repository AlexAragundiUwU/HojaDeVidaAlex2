#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos y aplicar migraciones
python manage.py collectstatic --no-input
python manage.py migrate

# Configurar el superusuario dinámicamente desde las variables de Render
echo "from django.contrib.auth import get_user_model; \
import os; \
User = get_user_model(); \
username = os.environ.get('DJANGO_SUPERUSER_USERNAME'); \
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD'); \
email = 'alexaragundi3050@gmail.com'; \
user, created = User.objects.get_or_create(username=username, defaults={'email': email}); \
user.set_password(password); \
user.is_superuser = True; \
user.is_staff = True; \
user.save(); \
print(f'Superusuario {username} actualizado/creado con exito')" \
| python manage.py shell