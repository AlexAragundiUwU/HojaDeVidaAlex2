from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# --- FORMULARIOS CON VALIDACIONES DE FECHAS ---

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
            raise ValidationError({'fechainiciogestion': "La fecha de inicio no puede ser una fecha futura."})
        if fin and fin > hoy:
            raise ValidationError({'fechafingestion': "La fecha de fin no puede ser una fecha futura."})
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafingestion': "La fecha de fin no puede ser anterior a la fecha de inicio."})
        return cleaned_data

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
            raise ValidationError({'fechainicio': "La fecha de inicio no puede ser una fecha futura."})
        if fin and fin > hoy:
            raise ValidationError({'fechafin': "La fecha de fin no puede ser una fecha futura."})
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafin': "La fecha de fin no puede ser anterior a la fecha de inicio."})
        return cleaned_data

class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fechainicio')
        fin = cleaned_data.get('fechafin')
        hoy = timezone.localdate()
        
        # Validación: No fechas futuras
        if inicio and inicio > hoy:
            raise ValidationError({'fechainicio': "La fecha de inicio no puede ser una fecha futura (ej. 2027)."})
        if fin and fin > hoy:
            raise ValidationError({'fechafin': "La fecha de finalización no puede ser una fecha futura."})
        
        # Validación: Coherencia cronológica (Fin no puede ser antes que Inicio)
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafin': f"Error: El producto terminó en {fin.year}, pero dices que inició en {inicio.year}. La fecha de fin debe ser posterior."})
            
        return cleaned_data

# --- CONFIGURACIÓN DEL PANEL ---

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('idperfil', 'nombres', 'apellidos', 'email_contacto', 'perfilactivo')
    list_editable = ('perfilactivo',)
    ordering = ('pk',)

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    form = ExperienciaLaboralForm
    list_display = ('idexperiencia', 'cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    form = CursosRealizadosForm
    list_display = ('idcursorealizado', 'nombrecurso', 'entidadpatrocinadora', 'estado_archivos', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

    def estado_archivos(self, obj):
        img = "✅ PNG" if obj.imagen_preview else "❌ Sin PNG"
        pdf = "✅ PDF" if obj.rutacertificado else "❌ Sin PDF"
        return format_html(f"<b>{img}</b> | <b>{pdf}</b>")
    estado_archivos.short_description = "Certificados"

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('idreconocimiento', 'descripcionreconocimiento', 'entidadpatrocinadora', 'fechareconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    form = ProductosAcademicosForm
    list_display = ('idproductoacademico', 'nombrerecurso', 'clasificador', 'fechainicio', 'fechafin', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('idproductolaboral', 'nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('idventagarage', 'nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto',)
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

# Títulos personalizados del panel
admin.site.site_header = "Administración del Portafolio"
admin.site.site_title = "Panel de Control Alex"
admin.site.index_title = "Gestión de Secciones y Currículum"