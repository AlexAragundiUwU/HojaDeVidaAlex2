import os
import dj_database_url
from pathlib import Path

# Directorio Base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ww9j7_=ac%06&-rvo27ci!8f)0^2)+o-m8@1+i^bxys)=%l0@2')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Render Hostnames
ALLOWED_HOSTS = ['*']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Aplicaciones - El orden es crítico
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',           # Debe ir antes de staticfiles
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
    'cloudinary',
    'Perfil',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProyectoHojaDeVida.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoHojaDeVida.wsgi.application'

# BASE DE DATOS
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# --- CONFIGURACIÓN DE CLOUDINARY Y STORAGES (CORREGIDO) ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Variable auxiliar para decidir el backend sin registrar DEFAULT_FILE_STORAGE
if CLOUDINARY_STORAGE['CLOUD_NAME'] and CLOUDINARY_STORAGE['API_KEY'] and CLOUDINARY_STORAGE['API_SECRET']:
    media_backend = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    media_backend = 'django.core.files.storage.FileSystemStorage'

# Configuración única para Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": media_backend,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Idioma y Hora
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil' 
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Permite cargar PDFs en iframes
X_FRAME_OPTIONS = 'SAMEORIGIN'