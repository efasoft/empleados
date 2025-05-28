"""   Creado por IA """

from django.db import models

class Empleado(models.Model):
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    edad = models.PositiveIntegerField()
    fecha_ingreso = models.DateField() # Renombrado para evitar conflicto con 'Fecha' como campo de entrada
    email = models.EmailField(unique=True)
    telefono_casa = models.CharField(max_length=20, blank=True, null=True)
    telefono_movil = models.CharField(max_length=20)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    sueldo_bruto = models.DecimalField(max_digits=10, decimal_places=2, editable=False) # Se calcula automáticamente
    password = models.CharField(max_length=128)  # Para almacenar el hash de la contraseña
    foto = models.ImageField(upload_to='empleados_fotos/', blank=False, null=False)
    is_deleted = models.BooleanField(default=False) # Para soft delete

    def save(self, *args, **kwargs):
        self.sueldo_bruto = self.sueldo_base + self.comision
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['apellidos', 'nombres']


