# ... (mantén las líneas de pip, collectstatic y migrate)

# RECREACIÓN FORZADA CON CLAVE SEGURA
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='Alex').delete(); \
user = User.objects.create_superuser('Alex', 'alexaragundi3050@gmail.com', 'Alex123456'); \
print('>>> USUARIO ALEX RECREADO CON CLAVE: Alex123456 <<<')" \
| python manage.py shell