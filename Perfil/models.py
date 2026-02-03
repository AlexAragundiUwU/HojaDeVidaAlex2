from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

def validar_no_futuro(value):
    """Evita que se ingresen fechas posteriores al día de hoy."""
    if value > date.today():
        raise ValidationError('La fecha no puede ser una fecha futura.')

class DatosPersonales(models.Model):
    idperfil = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Perfil"
    )
    nombres = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=100, null=True, blank=True)
    descripcionperfil = models.TextField(null=True, blank=True)
    fotoperfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    archivocv = models.FileField(upload_to='cv/', blank=True, null=True)
    email_contacto = models.EmailField(max_length=100, blank=True, null=True)
    telefonofijo = models.CharField(max_length=20, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=20, blank=True, null=True)
    sitioweb = models.CharField(max_length=100, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=200, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=200, blank=True, null=True)
    numerocedula = models.CharField(max_length=20, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    fechanacimiento = models.DateField(
        blank=True, 
        null=True, 
        validators=[validar_no_futuro],
        verbose_name="Fecha de Nacimiento"
    )
    lugarnacimiento = models.CharField(max_length=100, null=True, blank=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    estadocivil = models.CharField(max_length=20, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=20, blank=True, null=True)
    perfilactivo = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="Perfil Activo (0 o 1)"
    )
    
    mostrar_experiencia = models.BooleanField(default=True)
    mostrar_cursos = models.BooleanField(default=True)
    mostrar_logros = models.BooleanField(default=True)
    mostrar_academicos = models.BooleanField(default=True)
    mostrar_proyectos = models.BooleanField(default=True)
    mostrar_garage = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'datos_personales'
        verbose_name = "Dato Personal"
        verbose_name_plural = "Datos Personales"
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    idexperiencia = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Experiencia"
    )
    nombrempresa = models.CharField(max_length=100, null=True, blank=True)
    cargodesempenado = models.CharField(max_length=100, null=True, blank=True)
    descripcionfunciones = models.TextField(null=True, blank=True)
    fechainiciogestion = models.DateField(null=True, blank=True)
    fechafingestion = models.DateField(null=True, blank=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    rutacertificado = models.FileField(upload_to='experiencia/', blank=True, null=True, verbose_name="Certificado Laboral (PDF)")
    imagen_preview = models.ImageField(upload_to='experiencia/previews/', blank=True, null=True, verbose_name="Vista Previa (PNG/JPG)")

    class Meta:
        managed = True
        db_table = 'experiencia_laboral'
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencia Laboral"
        ordering = ['-fechainiciogestion', '-idexperiencia']

class Reconocimientos(models.Model):
    idreconocimiento = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Reconocimiento"
    )
    descripcionreconocimiento = models.CharField(max_length=255, null=True, blank=True)
    tiporeconocimiento = models.CharField(max_length=100, null=True, blank=True)
    entidadpatrocinadora = models.CharField(max_length=100, null=True, blank=True)
    fechareconocimiento = models.DateField(null=True, blank=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    rutacertificado = models.FileField(upload_to='reconocimientos/', blank=True, null=True, verbose_name="Certificado (PDF)")
    imagen_preview = models.ImageField(upload_to='reconocimientos/previews/', blank=True, null=True, verbose_name="Vista Previa (PNG/JPG)")

    class Meta:
        managed = True
        db_table = 'reconocimientos'
        verbose_name = "Reconocimiento"
        verbose_name_plural = "Reconocimientos"
        ordering = ['-fechareconocimiento', '-idreconocimiento']

class CursosRealizados(models.Model):
    idcursorealizado = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Curso"
    )
    nombrecurso = models.CharField(max_length=100, db_column='nombrerecurso', null=True, blank=True)
    entidadpatrocinadora = models.CharField(max_length=100, null=True, blank=True)
    fechainicio = models.DateField(null=True, blank=True)
    fechafin = models.DateField(null=True, blank=True)
    totalhoras = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name="Total Horas"
    )
    descripcioncurso = models.TextField(blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=20, blank=True, null=True)
    emailempresapatrocinadora = models.EmailField(blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    rutacertificado = models.FileField(upload_to='cursos/', blank=True, null=True, verbose_name="Certificado (PDF)")
    archivo_extra = models.FileField(upload_to='cursos/extra/', blank=True, null=True)
    imagen_preview = models.ImageField(upload_to='cursos/previews/', blank=True, null=True, verbose_name="Vista Previa (PNG/JPG)")

    class Meta:
        managed = True
        db_table = 'cursos_realizados'
        verbose_name = "Curso Realizado"
        verbose_name_plural = "Cursos Realizados"
        ordering = ['-fechafin', '-idcursorealizado']

class ProductosAcademicos(models.Model):
    idproductoacademico = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Académico"
    )
    nombrerecurso = models.CharField(max_length=100, null=True, blank=True)
    clasificador = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fechainicio = models.DateField(null=True, blank=True, verbose_name="Fecha Inicio")
    fechafin = models.DateField(null=True, blank=True, verbose_name="Fecha Fin")
    
    documento = models.FileField(upload_to='academicos/', blank=True, null=True, verbose_name="Documento (PDF)")
    imagen_preview = models.ImageField(upload_to='academicos/previews/', blank=True, null=True, verbose_name="Vista Previa (PNG/JPG)")
    
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'productos_academicos'
        verbose_name = "Producto Académico"
        verbose_name_plural = "Productos Académicos"
        ordering = ['-fechafin', '-idproductoacademico']

class ProductosLaborales(models.Model):
    idproductolaboral = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Proyecto"
    )
    nombreproducto = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fechaproducto = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'productos_laborales'
        verbose_name = "Proyecto Laboral"
        verbose_name_plural = "Proyectos Laborales"
        ordering = ['-fechaproducto', '-idproductolaboral']

class VentaGarage(models.Model):
    idventagarage = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="ID Garaje"
    )
    nombreproducto = models.CharField(max_length=100, null=True, blank=True)
    descripcionproducto = models.TextField(null=True, blank=True)
    valordelbien = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)], 
        verbose_name="Valor del Bien"
    )
    estadoproducto = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='garage/', blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'venta_garage'
        verbose_name = "Venta de Garaje"
        verbose_name_plural = "Venta de Garaje"