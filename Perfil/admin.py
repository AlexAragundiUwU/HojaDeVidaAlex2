from django.contrib import admin
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

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
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',) # Edición rápida

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento',)
    list_editable = ('activarparaqueseveaenfront',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
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