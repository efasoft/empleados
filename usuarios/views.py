"""   Creado por IA """

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'usuarios/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('usuarios:login')
    success_message = "Cuenta creada exitosamente. ¡Por favor, inicia sesión!"

    def form_invalid(self, form):
        # Muestra los errores de validación de Django en SweetAlert2
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en {field if field != '__all__' else 'formulario'}: {error}")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, '¡Bienvenido! Has iniciado sesión exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Has cerrado sesión exitosamente.')
        return super().dispatch(request, *args, **kwargs)