"""   Creado por IA """

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# CORRECTED: Añade field_validator y model_validator aquí
from pydantic import ValidationError, BaseModel, Field, model_validator, field_validator # <-- AQUI LA CORRECCIÓN
import re

# Pydantic model para validación de registro
class UserRegisterPydantic(BaseModel):
    username: str = Field(..., min_length=4, max_length=150)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8)
    password2: str

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password2:
            raise ValueError("Las contraseñas no coinciden.")
        return self

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean(self):
        cleaned_data = super().clean()
        try:
            # Validar con Pydantic
            user_data = {
                "username": cleaned_data.get('username'),
                "email": cleaned_data.get('email'),
                "password": cleaned_data.get('password2'), # Usamos password2 para la validación Pydantic
                "password2": cleaned_data.get('password2')
            }
            UserRegisterPydantic(**user_data)
        except ValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                message = error['msg']
                # Mapear los errores de Pydantic a los campos del formulario Django
                if field == 'password' or field == 'password2': # Ambos campos de password pueden generar errores
                    self.add_error('password2', message)
                elif field == 'email':
                    self.add_error('email', message)
                elif field == 'username':
                    self.add_error('username', message)
                else:
                    self.add_error(None, message) # Error general

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Django UserCreationForm ya hashea la contraseña, pero si la hubiéramos manipulado
        # con Pydantic y un campo diferente, necesitaríamos hacer make_password(cleaned_data['password2'])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Importación de FormHelper y Layout se hace en el archivo de vistas o en el template
        # si se usa {% crispy form %}. Si se renderiza manual, se hace aquí.
        # Por simplicidad y para no alargar más el error, asumo que Crispy Forms ya funciona.
        # Si tienes problemas con Crispy Forms, asegúrate de que sus importaciones
        # (FormHelper, Layout, Submit, etc.) también estén en este archivo si las usas directamente.
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('password', css_class='form-control', template='empleados/password_input.html'), # Reutilizamos el template
            HTML('<div class="mb-3"></div>'), # Espaciador
            Submit('submit', 'Iniciar Sesión', css_class='btn btn-primary mt-3'),
            HTML('<a href="{% url \'usuarios:register\' %}" class="btn btn-secondary mt-3 ms-2">Registrarse</a>')
        )