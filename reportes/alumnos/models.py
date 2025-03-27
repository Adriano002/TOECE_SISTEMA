from django.db import models
from django.utils.timezone import now


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, blank=True, null=True)
    grado = models.CharField(max_length=1)
    seccion = models.CharField(max_length=1, blank=True)
    nombredeseccion = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.grado} -{self.seccion} - {self.nombredeseccion} "


class Tutor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    apellido = models.CharField(max_length=100, unique=True)
    grado = models.CharField(max_length=1)
    seccion = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"


class Padre(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    estudiantes = models.ManyToManyField(
        'Estudiante', related_name='padres', blank=True)

    def __str__(self):
        return f"{self.nombre}"


class Madre(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    estudiantes = models.ManyToManyField(
        'Estudiante', related_name='madres', blank=True)

    def __str__(self):
        return f"{self.nombre}"


class Apoderado(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True)
    estudiantes = models.ManyToManyField(
        'Estudiante', related_name='apoderados', blank=True)

    def __str__(self):
        return f"{self.nombre}"


class Observacion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Observación de {self.estudiante}"


class AccionRespuesta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.nombre}"


class ReporteAlumno(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    padre = models.ForeignKey(
        Padre, on_delete=models.SET_NULL, null=True, blank=True)
    madre = models.ForeignKey(
        Madre, on_delete=models.SET_NULL, null=True, blank=True)
    apoderado = models.ForeignKey(
        Apoderado, on_delete=models.SET_NULL, null=True, blank=True)
    condicion = models.CharField(
        max_length=255,
        choices=[
            ("embarazo", "Embarazo"),
            ("madre_lactante", "Madre Lactante"),
            ("tratamiento_psiquiatrico", "Tratamiento Psiquiátrico"),
            ("certificado_medico", "Certificado Médico"),
            ("sustancias_psicoactivas", "Sustancias Psicoactivas"),
            ("evade_clases", "Evade Clases"),
            ("alcohol", "Consume Alcohol"),
            ("violencia", "Violencia"),
            ("siseve", "SISEVE"),
            ("tocamientos_indebidos", "Tocamientos Indebidos")
        ]
    )
    accion_respuesta = models.ForeignKey(
        AccionRespuesta, on_delete=models.SET_NULL, null=True, blank=True)
    tutor = models.ForeignKey(
        Tutor, on_delete=models.SET_NULL, null=True, blank=True)
    observacion = models.ForeignKey(
        Observacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        """ Guarda el reporte y lo asocia automáticamente al historial del estudiante """
        super().save(*args, **kwargs)  # Guarda el reporte primero

        # Verifica si el estudiante ya tiene un historial, si no, lo crea
        historial, creado = HistorialAlumno.objects.get_or_create(
            estudiante=self.estudiante)

        # Agrega el reporte actual al historial sin borrar los anteriores
        historial.reportes.add(self)

        # Guarda el historial actualizado
        historial.save()

    def __str__(self):
        return f"Reporte de {self.estudiante} - {self.condicion} - {self.fecha.strftime('%d/%m/%Y %H:%M:%S')}"


class HistorialAlumno(models.Model):
    estudiante = models.OneToOneField(
        Estudiante, on_delete=models.CASCADE, related_name='historial')
    reportes = models.ManyToManyField(ReporteAlumno, blank=True)
    fecha = models.DateTimeField(default=now)

    def actualizar_historial(self):
        """ Obtiene todos los reportes del estudiante y los agrega al historial """
        reportes_del_estudiante = ReporteAlumno.objects.filter(
            estudiante=self.estudiante)
        # Agregar todos los reportes
        self.reportes.set(reportes_del_estudiante)
        self.save()

    def __str__(self):
        return f"Historial de {self.estudiante} - {self.fecha.strftime('%d/%m/%Y %H:%M:%S')}"
