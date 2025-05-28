"""   Creado por IA """

from django.urls import path
from .views import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView

app_name = 'empleados'

urlpatterns = [
    path('', EmpleadoListView.as_view(), name='empleado_list'),
    path('crear/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
]