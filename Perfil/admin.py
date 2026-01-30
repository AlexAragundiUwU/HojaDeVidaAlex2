from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# --- FORMULARIOS PERSONALIZADOS CON VALIDACIONES ---

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainiciogestion')
        fin = cleaned_data.get('fechafingestion')
        
        # Obtenemos la fecha actual del servidor al momento de guardar
        hoy = timezone.now().date()

        # 1. Validación: Inicio no puede ser futuro
        if inicio and inicio > hoy:
            raise ValidationError({
                'fechainiciogestion': f"La fecha de inicio no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}."
            })

        # 2. Validación: Fin no puede ser futuro
        if fin and fin > hoy:
            raise ValidationError({
                'fechafingestion': f"La fecha de finalización no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}."
            })

        # 3. Validación Cronológica: Fin no puede ser antes que Inicio
        if inicio and fin and fin < inicio:
            raise ValidationError({
                'fechafingestion': "La fecha de finalización no puede ser anterior a la fecha de inicio."
            })
        
        return cleaned_data

class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainicio')
        fin = cleaned_data.get('fechafin')
        
        hoy = timezone.now().date()

        # 1. Inicio Futuro
        if inicio and inicio > hoy:
            raise ValidationError({
                'fechainicio': f"El curso no puede iniciar en el futuro. Hoy es {hoy.strftime('%d/%m/%Y')}."
            })
        
        # 2. Fin Futuro
        if fin and fin > hoy:
            raise ValidationError({
                'fechafin': f"El curso no puede terminar en el futuro. Hoy es {hoy.strftime('%d/%m/%Y')}."
            })

        # 3. Coherencia Temporal
        if inicio and fin and fin < inicio:
            raise ValidationError({
                'fechafin': "La fecha de finalización no puede ser anterior al inicio del curso."
            })

        return cleaned_data

class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = '__all__'

    def clean_fechareconocimiento(self):
        fecha = self.cleaned_data.get('fechareconocimiento')
        hoy = timezone.now().date()
        
        # 1. Fecha Futura
        if fecha and fecha > hoy:
            raise ValidationError(f"La fecha del reconocimiento no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}.")
        return fecha


# --- CONFIGURACIÓN DEL ADMIN ---

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display = ('nombres', 'apellidos', 'numerocedula', 'email_contacto', 'perfilactivo')
    # Permite cambiar el perfil activo directamente desde la lista
    list_editable = ('perfilactivo',)
    
    # Organización del formulario en grupos (Fieldsets)
    fieldsets = (
        ('Información Principal', {
            'fields': (
                'idperfil', 'fotoperfil', 'archivocv', 
                'nombres', 'apellidos', 'descripcionperfil', 
                'perfilactivo'
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'email_contacto', 'telefonofijo', 'telefonoconvencional', 
                'sitioweb', 'direcciondomiciliaria', 'direcciontrabajo'
            )
        }),
        ('Detalles Personales', {
            'fields': (
                'numerocedula', 'nacionalidad', 'fechanacimiento', 'lugarnacimiento',
                'sexo', 'estadocivil', 'licenciaconducir'
            )
        }),
        # SECCIÓN NUEVA: Interruptores para ocultar/mostrar paneles en el Home
        ('Control de Visibilidad', {
            'fields': (
                'mostrar_experiencia', 
                'mostrar_cursos', 
                'mostrar_logros', 
                'mostrar_academicos', 
                'mostrar_proyectos', 
                'mostrar_garage'
            ),
            'description': 'Marca o desmarca las casillas para mostrar u ocultar las secciones en la página web.'
        }),
    )
    
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    form = ExperienciaLaboralForm  # Conectamos la validación
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',) # Edición rápida

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    form = ReconocimientosForm  # Conectamos la validación
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento',)
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    form = CursosRealizadosForm  # Conectamos la validación
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    # Agregamos 'imagen' para confirmar visualmente que se cargó
    list_display = ('nombreproducto', 'fechaproducto', 'imagen', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)