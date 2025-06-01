"""   Creado por IA """

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Empleado
from .forms import EmpleadoForm
from django.contrib import messages
from django.http import JsonResponse
from django.views import View

class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10 # Paginación
    
    def get_queryset(self):
        return Empleado.objects.filter(is_deleted=False) # Solo mostrar empleados no eliminados

class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form.html'
    success_url = reverse_lazy('empleados:empleado_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empleado creado exitosamente!')
        return response

    def form_invalid(self, form):
        # SweetAlert2 se manejará en el frontend con JavaScript
        errors = {field: [str(e) for e in errors] for field, errors in form.errors.items()}
        # Añade un mensaje general para SweetAlert2 en el template
        messages.error(self.request, "Hay errores en el formulario. Por favor, corrígelos.")
        return super().form_invalid(form)


class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form.html'
    success_url = reverse_lazy('empleados:empleado_list')

    def get_object(self, queryset=None):
        # Asegurarse de que no se pueda editar un empleado "soft deleted"
        obj = get_object_or_404(Empleado, pk=self.kwargs['pk'], is_deleted=False)
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Empleado actualizado exitosamente!')
        return response

    def form_invalid(self, form):
        errors = {field: [str(e) for e in errors] for field, errors in form.errors.items()}
        messages.error(self.request, "Hay errores en el formulario. Por favor, corrígelos.")
        return super().form_invalid(form)


class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'empleado_confirm_delete.html'
    success_url = reverse_lazy('empleados:empleado_list')

    def get_object(self, queryset=None):
        # Asegurarse de que no se pueda borrar permanentemente un empleado ya "soft deleted"
        obj = get_object_or_404(Empleado, pk=self.kwargs['pk'], is_deleted=False)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True # Soft delete
        self.object.save()
        messages.success(self.request, 'Empleado eliminado (soft delete) exitosamente!')
        return redirect(self.get_success_url())