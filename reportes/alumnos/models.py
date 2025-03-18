from django.db import models
from django.utils.timezone import now

# Tabla de Estudiantes


class Estudiante(models.Model):
    dni = models.CharField(max_length=8, blank=True)
    nombre = models.CharField(max_length=100, unique=True)
    grado = models.CharField(max_length=1)
    seccion = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.dni} - {self.nombre}"

# tabla tutor


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
        'Estudiante', related_name='padres')  # Relación con estudiantes


class Madre(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    estudiantes = models.ManyToManyField(
        'Estudiante', related_name='madres')  # Relación con estudiantes


class Apoderado(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True, null=True)
    estudiantes = models.ManyToManyField(
        'Estudiante', related_name='apoderados')  # Relación con estudiantes


class Observacion(models.Model):
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    estudiante = models.ForeignKey(
        # Permitir valores nulos
        'Estudiante', on_delete=models.CASCADE, related_name='observaciones', null=True, blank=True
    )


# Tabla de Acciones de Respuesta


class AccionRespuesta(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Accion tomada {self.nombre}"


# Tabla de Historial de Alumnos


class ReporteAlumno(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE)  # Obligatorio
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
    )  # Obligatorio
    accion_respuesta = models.ForeignKey(
        AccionRespuesta, on_delete=models.SET_NULL, null=True, blank=True)
    tutor = models.ForeignKey(
        Tutor, on_delete=models.SET_NULL, null=True, blank=True)
    observacion = models.ForeignKey(
        Observacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_reporte = models.DateTimeField(default=now)  # 🕒 Guarda fecha y hora

    def __str__(self):
        return f"Reporte de {self.estudiante} - {self.condicion} ({self.fecha_reporte.strftime('%d/%m/%Y %H:%M')})"


class HistorialAlumno(models.Model):
    estudiante = models.OneToOneField(
        Estudiante, on_delete=models.CASCADE, related_name='historial')
    reportes = models.ManyToManyField(
        ReporteAlumno, blank=True)  # Relación con reportes

    def actualizar_historial(self):
        """Actualizar el historial con los reportes existentes del estudiante."""
        reportes_del_estudiante = ReporteAlumno.objects.filter(
            estudiante=self.estudiante)
        # Asigna los reportes al historial
        self.reportes.set(reportes_del_estudiante)
        self.save()

    def __str__(self):
        return f"Historial de {self.estudiante}"
