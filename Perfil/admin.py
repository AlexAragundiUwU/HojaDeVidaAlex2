from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# --- FORMULARIOS ---
class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainicio')
        fin = cleaned_data.get('fechafin')
        hoy = timezone.localdate()
        if inicio and inicio > hoy: raise ValidationError({'fechainicio': "Fecha futura no permitida."})
        if fin and fin > hoy: raise ValidationError({'fechafin': "Fecha futura no permitida."})
        return cleaned_data

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainiciogestion')
        fin = cleaned_data.get('fechafingestion')
        hoy = timezone.localdate()
        if inicio and inicio > hoy: raise ValidationError({'fechainiciogestion': "Fecha futura no permitida."})
        if fin and fin > hoy: raise ValidationError({'fechafingestion': "Fecha futura no permitida."})
        return cleaned_data

# --- CONFIGURACIÓN ADMIN ---

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('idperfil', 'nombres', 'apellidos', 'email_contacto', 'perfilactivo')
    list_editable = ('perfilactivo',)
    ordering = ('pk',)
    # IMPORTANTE: Agregamos idperfil a readonly_fields para que se vea dentro del formulario
    readonly_fields = ('idperfil',) 
    
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
    form = ExperienciaLaboralForm
    list_display = ('idexperiencia', 'cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idexperiencia',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    form = CursosRealizadosForm
    list_display = ('idcursorealizado', 'nombrecurso', 'entidadpatrocinadora', 'estado_archivos', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idcursorealizado',)

    def estado_archivos(self, obj):
        img = "✅ PNG" if obj.imagen_preview else "❌ Sin PNG"
        pdf = "✅ PDF" if obj.rutacertificado else "❌ Sin PDF"
        return format_html(f"<b>{img}</b> | <b>{pdf}</b>")
    estado_archivos.short_description = "Archivos"

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('idreconocimiento', 'descripcionreconocimiento', 'entidadpatrocinadora', 'estado_archivos', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idreconocimiento',)

    def estado_archivos(self, obj):
        img = "✅ PNG" if obj.imagen_preview else "❌ Sin PNG"
        pdf = "✅ PDF" if obj.rutacertificado else "❌ Sin PDF"
        return format_html(f"<b>{img}</b> | <b>{pdf}</b>")
    estado_archivos.short_description = "Archivos"

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('idproductoacademico', 'nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idproductoacademico',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('idproductolaboral', 'nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idproductolaboral',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('idventagarage', 'nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto',)
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)
    # Mostrar ID dentro del formulario
    readonly_fields = ('idventagarage',)

# Títulos del Admin
admin.site.site_header = "Panel de Administración"
admin.site.site_title = "Admin Alex"
admin.site.index_title = "Gestión de Portafolio"