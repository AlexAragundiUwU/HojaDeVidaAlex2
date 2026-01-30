from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# --- FORMULARIOS CON VALIDACIÓN DE FECHA (Evita fechas futuras) ---
class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainicio')
        fin = cleaned_data.get('fechafin')
        hoy = timezone.localdate()
        
        if inicio and inicio > hoy:
            raise ValidationError({'fechainicio': f"La fecha de inicio no puede ser futura. Hoy es {hoy}."})
        if fin and fin > hoy:
            raise ValidationError({'fechafin': f"La fecha de finalización no puede ser futura. Hoy es {hoy}."})
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafin': "La fecha de fin no puede ser anterior a la de inicio."})
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
        
        if inicio and inicio > hoy:
            raise ValidationError({'fechainiciogestion': f"Fecha de inicio futura no permitida."})
        if fin and fin > hoy:
            raise ValidationError({'fechafingestion': f"Fecha de fin futura no permitida."})
        return cleaned_data

# --- CONFIGURACIÓN DEL PANEL DE ADMINISTRACIÓN ---

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    form = CursosRealizadosForm
    # list_display: Columnas que verás en la tabla principal
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'estado_archivos', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    # ordering = ('pk',): Solución definitiva al error "Cannot resolve keyword 'id'"
    ordering = ('-pk',)

    def estado_archivos(self, obj):
        """Muestra de forma visual si subiste el PNG y el PDF"""
        img = "✅ PNG" if obj.imagen_preview else "❌ Sin PNG"
        pdf = "✅ PDF" if obj.rutacertificado else "❌ Sin PDF"
        return format_html(f"<b>{img}</b> | <b>{pdf}</b>")
    
    estado_archivos.short_description = "Archivos (Vista/Descarga)"

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'entidadpatrocinadora', 'estado_archivos', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('-pk',)

    def estado_archivos(self, obj):
        img = "✅ PNG" if obj.imagen_preview else "❌ Sin PNG"
        pdf = "✅ PDF" if obj.rutacertificado else "❌ Sin PDF"
        return format_html(f"<b>{img}</b> | <b>{pdf}</b>")
    
    estado_archivos.short_description = "Archivos (Vista/Descarga)"

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email_contacto', 'perfilactivo')
    list_editable = ('perfilactivo',)
    ordering = ('pk',)

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    form = ExperienciaLaboralForm
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('-fechainiciogestion',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('-pk',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('-fechaproducto',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto',)
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

# --- PERSONALIZACIÓN GLOBAL DEL TÍTULO ---
admin.site.site_header = "Panel de Administración"
admin.site.site_title = "Admin Alex"
admin.site.index_title = "Bienvenido a la Gestión de tu Portafolio Profesional"