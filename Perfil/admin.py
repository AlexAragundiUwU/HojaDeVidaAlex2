from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html
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
        
        hoy = timezone.localdate()

        if inicio and inicio > hoy:
            raise ValidationError({'fechainiciogestion': f"La fecha de inicio no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}."})
        if fin and fin > hoy:
            raise ValidationError({'fechafingestion': f"La fecha de finalización no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}."})
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafingestion': "La fecha de finalización no puede ser anterior a la fecha de inicio."})
        
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
            raise ValidationError({'fechainicio': f"El curso no puede iniciar en el futuro. Hoy es {hoy.strftime('%d/%m/%Y')}."})
        if fin and fin > hoy:
            raise ValidationError({'fechafin': f"El curso no puede terminar en el futuro. Hoy es {hoy.strftime('%d/%m/%Y')}."})
        if inicio and fin and fin < inicio:
            raise ValidationError({'fechafin': "La fecha de finalización no puede ser anterior al inicio del curso."})

        return cleaned_data

class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = '__all__'

    def clean_fechareconocimiento(self):
        fecha = self.cleaned_data.get('fechareconocimiento')
        hoy = timezone.localdate()
        if fecha and fecha > hoy:
            raise ValidationError(f"La fecha del reconocimiento no puede ser futura. Hoy es {hoy.strftime('%d/%m/%Y')}.")
        return fecha


# --- CONFIGURACIÓN DEL ADMIN ---

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'email_contacto', 'perfilactivo')
    list_editable = ('perfilactivo',)
    ordering = ('pk',) # Ordenar por PK para evitar error de ID
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('idperfil', 'fotoperfil', 'archivocv', 'nombres', 'apellidos', 'descripcionperfil', 'perfilactivo')
        }),
        ('Información de Contacto', {
            'fields': ('email_contacto', 'telefonofijo', 'telefonoconvencional', 'sitioweb', 'direcciondomiciliaria', 'direcciontrabajo')
        }),
        ('Detalles Personales', {
            'fields': ('numerocedula', 'nacionalidad', 'fechanacimiento', 'lugarnacimiento', 'sexo', 'estadocivil', 'licenciaconducir')
        }),
        ('Control de Visibilidad', {
            'fields': ('mostrar_experiencia', 'mostrar_cursos', 'mostrar_logros', 'mostrar_academicos', 'mostrar_proyectos', 'mostrar_garage'),
            'description': 'Marca o desmarca las casillas para mostrar u ocultar las secciones en la página web.'
        }),
    )
    
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    form = ExperienciaLaboralForm
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    form = ReconocimientosForm
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'vista_previa_certificado', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento',)
    list_editable = ('activarparaqueseveaenfront',)
    readonly_fields = ('vista_previa_certificado',)
    ordering = ('pk',) # CRUCIAL: Evita el error "Cannot resolve keyword 'id'"

    def vista_previa_certificado(self, obj):
        try:
            if obj and obj.certificado:
                url = obj.certificado.url
                if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                     return format_html('<a href="{}" target="_blank"><img src="{}" width="100" style="border-radius: 5px; border: 1px solid #ccc;" /></a>', url, url)
                else:
                     return format_html('<a href="{}" target="_blank" class="button">Ver Archivo</a>', url)
        except Exception:
            return "Error al cargar vista previa"
        return "Guarda para ver la vista previa"
    
    vista_previa_certificado.short_description = "Vista Previa"

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    form = CursosRealizadosForm
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'vista_previa_certificado', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    readonly_fields = ('vista_previa_certificado',)
    ordering = ('pk',) # CRUCIAL: Evita el error "Cannot resolve keyword 'id'"

    def vista_previa_certificado(self, obj):
        try:
            if obj and obj.certificado:
                url = obj.certificado.url
                if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                     return format_html('<a href="{}" target="_blank"><img src="{}" width="100" style="border-radius: 5px; border: 1px solid #ccc;" /></a>', url, url)
                else:
                     return format_html('<a href="{}" target="_blank" class="button">Ver Archivo</a>', url)
        except Exception:
             return "Error al cargar vista previa"
        return "Guarda para ver la vista previa"

    vista_previa_certificado.short_description = "Vista Previa"

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'vista_previa_imagen', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    readonly_fields = ('vista_previa_imagen',)
    ordering = ('pk',)

    def vista_previa_imagen(self, obj):
        try:
            if obj and obj.imagen:
                return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.imagen.url)
        except:
            return "-"
        return "-"
    vista_previa_imagen.short_description = "Imagen"

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    ordering = ('pk',)

# --- PERSONALIZACIÓN DEL TÍTULO DEL PANEL ---
admin.site.site_header = "Panel de Administración"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Panel de Administración"
