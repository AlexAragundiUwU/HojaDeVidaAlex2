#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario solo si no existe
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='Alex').exists() or \
User.objects.create_superuser('Alex', 'alexaragundi3050@gmail.com', '123456')" \
| python manage.py shell