#!/usr/bin/env bash
# Salir si hay un error
set -o errexit

# Instalación de librerías
pip install -r requirements.txt

# Recolección de estáticos y aplicación de tablas
python manage.py collectstatic --no-input
python manage.py migrate

# Configuración del superusuario Alex con la clave 1234
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
user, created = User.objects.get_or_create(username='Alex', defaults={'email': 'alexaragundi3050@gmail.com'}); \
user.set_password('1234'); \
user.is_superuser = True; \
user.is_staff = True; \
user.save(); \
print('Superusuario Alex configurado con exito con la clave 1234')" \
| python manage.py shell