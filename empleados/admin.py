"""   Creado por IA """

from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'nombres', 'apellidos', 'edad', 'fecha_ingreso', 'email',
        'telefono_movil', 'sueldo_base', 'comision', 'sueldo_bruto', 'is_deleted'
    )
    list_filter = ('is_deleted', 'edad', 'fecha_ingreso')
    search_fields = ('nombres', 'apellidos', 'email', 'telefono_movil')
    readonly_fields = ('sueldo_bruto',) # Sueldo bruto es calculado

    def get_queryset(self, request):
        # Permite ver también los empleados eliminados suavemente en el admin
        return self.model.objects.all()

    def delete_model(self, request, obj):
        # Implementa soft delete también desde el admin (opcional)
        obj.is_deleted = True
        obj.save()
