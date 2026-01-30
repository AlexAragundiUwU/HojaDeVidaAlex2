from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

# --- FUNCIÓN DE RESCATE ---
def crear_superusuario_emergencia(request):
    try:
        # 1. Borramos al usuario Alex si existe (para limpiar errores previos)
        if User.objects.filter(username='Alex').exists():
            User.objects.get(username='Alex').delete()
        
        # 2. Creamos el usuario limpio
        User.objects.create_superuser('Alex', 'alexaragundi3050@gmail.com', 'Alex1234')
        
        return HttpResponse("""
            <h1 style='color:green'>¡ÉXITO! USUARIO CREADO</h1>
            <p>Ya puedes entrar al admin.</p>
            <ul>
                <li>Usuario: <b>Alex</b></li>
                <li>Contraseña: <b>Alex1234</b></li>
            </ul>
            <a href='/admin/'>Ir al Login ahora</a>
        """)
    except Exception as e:
        return HttpResponse(f"<h1 style='color:red'>Error: {str(e)}</h1>")
# --------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta es tu ruta secreta de rescate:
    path('rescate-alex/', crear_superusuario_emergencia),
    
    # Tus otras rutas (mantén las que ya tenías, como la de Perfil)
    path('', include('Perfil.urls')), 
]

# Configuración para archivos media (imágenes)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)