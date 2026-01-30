from django.shortcuts import render, redirect
from .models import (
    DatosPersonales, ExperienciaLaboral, 
    CursosRealizados, VentaGarage,
    Reconocimientos, ProductosAcademicos, ProductosLaborales
)

# Función auxiliar para obtener el perfil que tiene el check de 'activo'
def get_active_profile():
    try:
        return DatosPersonales.objects.filter(perfilactivo=1).first()
    except:
        return None

def home(request):
    perfil = get_active_profile()
    
    # Lógica para ocultar secciones permanentemente desde la "X" de las tarjetas
    if perfil:
        campo_a_ocultar = request.GET.get('ocultar')
        if campo_a_ocultar and hasattr(perfil, campo_a_ocultar):
            setattr(perfil, campo_a_ocultar, False)
            perfil.save()
            return redirect('home')

    # Inicialización de contadores
    c_exp = c_cur = c_log = c_aca = c_pro = c_gar = 0
    
    if perfil:
        # Conteo de registros activos para mostrar en las burbujas de las tarjetas
        c_exp = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_cur = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_log = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_aca = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_pro = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()
        c_gar = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).count()

    context = {
        'perfil': perfil,
        # Resúmenes limitados a 3 registros y ORDENADOS CRONOLÓGICAMENTE
        'resumen_exp': ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechainiciogestion')[:3] if perfil else [],

        'resumen_cursos': CursosRealizados.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechafin')[:3] if perfil else [],

        'resumen_garage': VentaGarage.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )[:5] if perfil else [],

        'resumen_rec': Reconocimientos.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechareconocimiento')[:3] if perfil else [],

        # CORRECCIÓN AQUÍ: Usamos 'pk' que es el alias universal para la clave primaria, 
        # o el nombre específico del campo si 'pk' fallara (pero pk es seguro en Django).
        # Para ProductosAcademicos, el error sugería 'idproductoacademico'.
        'resumen_acad': ProductosAcademicos.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-pk')[:3] if perfil else [],

        'resumen_lab': ProductosLaborales.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechaproducto')[:3] if perfil else [],
        
        # Totales para el modal y las burbujas
        'total_exp': c_exp, 'total_cursos': c_cur, 'total_logros': c_log,
        'total_acad': c_aca, 'total_proyectos': c_pro, 'total_garage': c_gar,
    }
    return render(request, 'home.html', context)

def vista_previa_cv(request):
    perfil = get_active_profile()
    if not perfil: 
        return redirect('home')

    context = {'perfil': perfil}
    
    # Lógica de filtros: recibe los parámetros del JavaScript del modal de home.html
    if request.GET.get('cv') == 'true': 
        context['incluir_perfil'] = True
        
    if request.GET.get('experiencia') == 'true': 
        context['experiencia'] = ExperienciaLaboral.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechainiciogestion')
        
    if request.GET.get('cursos') == 'true': 
        context['cursos'] = CursosRealizados.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechafin')
        
    if request.GET.get('logros') == 'true': 
        context['logros'] = Reconocimientos.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechareconocimiento')
        
    if request.GET.get('proyectos') == 'true': 
        context['proyectos'] = ProductosLaborales.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-fechaproducto')
        
    if request.GET.get('garage') == 'true': 
        context['garage'] = VentaGarage.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        )
    
    if request.GET.get('academicos') == 'true': 
        # CORRECCIÓN AQUÍ TAMBIÉN
        context['academicos'] = ProductosAcademicos.objects.filter(
            idperfilconqueestaactivo=perfil, 
            activarparaqueseveaenfront=True
        ).order_by('-pk')

    return render(request, 'cv_print.html', context)

# Vistas de las páginas individuales (CON ORDENAMIENTO)
def experiencia(request):
    perfil = get_active_profile()
    datos = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ).order_by('-fechainiciogestion') if perfil else []
    return render(request, 'experiencia.html', {'datos': datos, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    # CORRECCIÓN AQUÍ TAMBIÉN
    datos = ProductosAcademicos.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ).order_by('-pk') if perfil else []
    return render(request, 'productos_academicos.html', {'datos': datos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    datos = ProductosLaborales.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto') if perfil else []
    return render(request, 'productos_laborales.html', {'datos': datos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    datos = CursosRealizados.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ).order_by('-fechafin') if perfil else []
    return render(request, 'cursos.html', {'datos': datos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    datos = Reconocimientos.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ).order_by('-fechareconocimiento') if perfil else []
    return render(request, 'reconocimientos.html', {'datos': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    datos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil, 
        activarparaqueseveaenfront=True
    ) if perfil else []
    return render(request, 'garage.html', {'datos': datos, 'perfil': perfil})