
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from .models import AccionRespuesta, Apoderado, Tutor, Estudiante, HistorialAlumno, Madre, Observacion, Padre, ReporteAlumno


@admin.register(AccionRespuesta)
class AccionRespuestaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    search_fields = ('dni', 'nombre', 'grado', 'seccion')


@admin.register(HistorialAlumno)
class HistorialAlumnoAdmin(admin.ModelAdmin):
    search_fields = ('estudiante__nombre', 'descripcion')


@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'celular', 'mostrar_estudiantes')

    def mostrar_estudiantes(self, obj):
        return ", ".join([e.nombre for e in obj.estudiantes.all()])
    mostrar_estudiantes.short_description = "Estudiantes"


@admin.register(Madre)
class MadreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'celular', 'mostrar_estudiantes')

    def mostrar_estudiantes(self, obj):
        return ", ".join([e.nombre for e in obj.estudiantes.all()])
    mostrar_estudiantes.short_description = "Estudiantes"


@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'celular', 'mostrar_estudiantes')

    def mostrar_estudiantes(self, obj):
        return ", ".join([e.nombre for e in obj.estudiantes.all()])
    mostrar_estudiantes.short_description = "Estudiantes"


@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'fecha', 'estudiante')


@admin.register(ReporteAlumno)
class ReporteAlumnoAdmin(admin.ModelAdmin):
    search_fields = ('estudiante__nombre', 'condicion', 'fecha_reporte')


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'grado', 'seccion')


@receiver(post_save, sender=ReporteAlumno)
def actualizar_historial_al_guardar_reporte(sender, instance, **kwargs):
    """Cada vez que se guarda un ReporteAlumno, se actualiza el historial del estudiante."""
    historial, creado = HistorialAlumno.objects.get_or_create(
        estudiante=instance.estudiante)
    historial.actualizar_historial()
