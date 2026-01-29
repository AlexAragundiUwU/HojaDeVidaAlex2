# ... (deja las líneas de pip install, collectstatic y migrate como están)

# BORRAR Y RECREAR SUPERUSUARIO (Solución definitiva)
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='Alex').delete(); \
User.objects.create_superuser('Alex', 'alexaragundi3050@gmail.com', '1234'); \
print('>>> USUARIO ALEX CREADO DESDE CERO CON CLAVE 1234 <<<')" \
| python manage.py shell