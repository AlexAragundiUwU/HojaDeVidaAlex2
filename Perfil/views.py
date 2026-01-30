from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os

# Importación de los modelos necesarios para el portafolio
from .models import (
    DatosPersonales, ExperienciaLaboral, CursosRealizados, 
    Reconocimientos, ProductosAcademicos, ProductosLaborales, VentaGarage
)

def link_callback(uri, rel):
    """
    Función para xhtml2pdf que convierte las URLs de archivos (media/static) 
    en rutas locales absolutas para que el generador de PDF encuentre las imágenes.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        return uri
    return path

def get_active_profile():
    """Recupera el perfil que tiene el campo perfilactivo marcado como 1."""
    try:
        return DatosPersonales.objects.filter(perfilactivo=1).first()
    except:
        return None

def home(request):
    """Vista principal que gestiona el resumen de las 6 secciones y el ocultado de tarjetas."""
    perfil = get_active_profile()
    
    if perfil:
        campo_a_ocultar = request.GET.get('ocultar')
        if campo_a_ocultar and hasattr(perfil, campo_a_ocultar):
            setattr(perfil, campo_a_ocultar, False)
            perfil.save()
            return redirect('home')

    c_exp = c_cur = c_log = c_aca = c_pro = c_gar = 0
    
    if perfil:
        c_exp = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_cur = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_log = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_aca = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_pro = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_gar = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()

    context = {
        'perfil': perfil,
        'resumen_exp': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechainiciogestion')[:3] if perfil else [],
        'resumen_cursos': CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechafin')[:3] if perfil else [],
        'resumen_rec': Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechareconocimiento')[:3] if perfil else [],
        'resumen_acad': ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-pk')[:3] if perfil else [],
        'resumen_lab': ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechaproducto')[:3] if perfil else [],
        'resumen_garage': VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:5] if perfil else [],
        'total_exp': c_exp, 'total_cursos': c_cur, 'total_logros': c_log,
        'total_acad': c_aca, 'total_proyectos': c_pro, 'total_garage': c_gar,
    }
    return render(request, 'home.html', context)

def vista_previa_cv(request):
    """Genera el PDF dinámico basándose en los filtros seleccionados."""
    perfil = get_active_profile()
    if not perfil:
        return redirect('home')

    context = {'perfil': perfil}

    if request.GET.get('experiencia') == 'true': 
        context['experiencias'] = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechainiciogestion')
        
    if request.GET.get('cursos') == 'true': 
        context['cursos'] = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechafin')
        
    if request.GET.get('logros') == 'true': 
        context['logros'] = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechareconocimiento')
        
    if request.GET.get('proyectos') == 'true': 
        context['proyectos'] = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechaproducto')
        
    if request.GET.get('garage') == 'true': 
        context['garage'] = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    
    if request.GET.get('academicos') == 'true': 
        context['academicos'] = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-pk')

    template = get_template('cv_print.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.nombres}_{perfil.apellidos}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('Error al procesar el PDF.')
    return response

# Vistas de detalle
def experiencia(request):
    perfil = get_active_profile()
    datos = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechainiciogestion') if perfil else []
    return render(request, 'experiencia.html', {'datos': datos, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    datos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-pk') if perfil else []
    return render(request, 'productos_academicos.html', {'datos': datos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    datos = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechaproducto') if perfil else []
    return render(request, 'productos_laborales.html', {'datos': datos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    datos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechafin') if perfil else []
    return render(request, 'cursos.html', {'datos': datos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    datos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechareconocimiento') if perfil else []
    return render(request, 'reconocimientos.html', {'datos': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    datos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True) if perfil else []
    return render(request, 'garage.html', {'datos': datos, 'perfil': perfil})