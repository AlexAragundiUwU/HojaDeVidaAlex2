from django.db import models

class DatosPersonales(models.Model):
    # CAMBIO: IntegerField para que sea editable
    idperfil = models.IntegerField(primary_key=True, verbose_name="ID Perfil")
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
    fechanacimiento = models.DateField(blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    estadocivil = models.CharField(max_length=20, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=20, blank=True, null=True)
    perfilactivo = models.IntegerField(blank=True, null=True)
    
    mostrar_experiencia = models.BooleanField(default=True)
    mostrar_cursos = models.BooleanField(default=True)
    mostrar_logros = models.BooleanField(default=True)
    mostrar_academicos = models.BooleanField(default=True)
    mostrar_proyectos = models.BooleanField(default=True)
    mostrar_garage = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'datos_personales'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    # CAMBIO: IntegerField
    idexperiencia = models.IntegerField(primary_key=True, verbose_name="ID Experiencia")
    nombrempresa = models.CharField(max_length=100, null=True, blank=True)
    cargodesempenado = models.CharField(max_length=100, null=True, blank=True)
    descripcionfunciones = models.TextField(null=True, blank=True)
    fechainiciogestion = models.DateField(null=True, blank=True)
    fechafingestion = models.DateField(null=True, blank=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'experiencia_laboral'

class Reconocimientos(models.Model):
    # CAMBIO: IntegerField
    idreconocimiento = models.IntegerField(primary_key=True, verbose_name="ID Reconocimiento")
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

class CursosRealizados(models.Model):
    # CAMBIO: IntegerField
    idcursorealizado = models.IntegerField(primary_key=True, verbose_name="ID Curso")
    nombrecurso = models.CharField(max_length=100, db_column='nombrerecurso', null=True, blank=True)
    entidadpatrocinadora = models.CharField(max_length=100, null=True, blank=True)
    fechainicio = models.DateField(null=True, blank=True)
    fechafin = models.DateField(null=True, blank=True)
    totalhoras = models.IntegerField(null=True, blank=True)
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

class ProductosAcademicos(models.Model):
    # CAMBIO: IntegerField
    idproductoacademico = models.IntegerField(primary_key=True, verbose_name="ID Académico")
    nombrerecurso = models.CharField(max_length=100, null=True, blank=True)
    clasificador = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    documento = models.FileField(upload_to='academicos/', blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'productos_academicos'

class ProductosLaborales(models.Model):
    # CAMBIO: IntegerField
    idproductolaboral = models.IntegerField(primary_key=True, verbose_name="ID Proyecto")
    nombreproducto = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fechaproducto = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'productos_laborales'

class VentaGarage(models.Model):
    # CAMBIO: IntegerField
    idventagarage = models.IntegerField(primary_key=True, verbose_name="ID Garaje")
    nombreproducto = models.CharField(max_length=100, null=True, blank=True)
    descripcionproducto = models.TextField(null=True, blank=True)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estadoproducto = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='garage/', blank=True, null=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, models.DO_NOTHING, db_column='idperfilconqueestaactivo', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'venta_garage'