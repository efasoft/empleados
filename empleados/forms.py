"""   Creado por IA """

from django import forms
from .models import Empleado
from .pydantic_models import EmpleadoPydantic, ValidationError
from django.contrib.auth.hashers import make_password, check_password # Para hashing de contraseñas
import decimal # Para manejar DecimalField correctamente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML

class EmpleadoForm(forms.ModelForm):
    # Campos que Pydantic validará, pero los manejamos como CharField para la entrada de texto
    # y luego los limpiamos para convertirlos al tipo de dato adecuado.
    nombres = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Nombres'}))
    apellidos = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    edad = forms.IntegerField(min_value=1, max_value=100, widget=forms.NumberInput(attrs={'placeholder': 'Edad'}))
    fecha_ingreso = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD-MM-AAAA'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'correo@example.com'}))
    telefono_casa = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': '+34 9XX XX XX XX'}))
    telefono_movil = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '+34 6XX XXX XXX'}))
    sueldo_base = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ej: 2.500,00'}))
    comision = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ej: 150,75'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'}
        )
    )
    foto = forms.ImageField(required=True)

    class Meta:
        model = Empleado
        fields = [
            'nombres', 'apellidos', 'edad', 'fecha_ingreso', 'email',
            'telefono_casa', 'telefono_movil', 'sueldo_base', 'comision',
            'password', 'foto'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombres', css_class='form-group col-md-6 mb-0'),
                Column('apellidos', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('edad', css_class='form-group col-md-4 mb-0'),
                Column('fecha_ingreso', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono_casa', css_class='form-group col-md-6 mb-0'),
                Column('telefono_movil', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('sueldo_base', css_class='form-group col-md-6 mb-0'),
                Column('comision', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('password', css_class='form-control', template='empleados/password_input.html'), # Custom template for password field
            HTML('<div class="mb-3"></div>'), # Espaciador
            Field('foto', css_class='form-control'),
            HTML('<div class="mb-3"></div>'), # Espaciador
            Submit('submit', 'Guardar', css_class='btn btn-primary mt-3'),
            HTML('<a href="{% url \'empleados:empleado_list\' %}" class="btn btn-secondary mt-3 ms-2">Cancelar</a>')
        )

        # Si estamos editando, no queremos mostrar la contraseña actual en el campo de texto
        # y manejamos la foto de manera diferente si ya existe.
        if self.instance.pk:
            self.fields['password'].required = False # Si edita, la contraseña no es obligatoria
            if self.instance.foto:
                # Esto es un truco simple. En un caso real, la gestión de fotos existentes
                # sería más sofisticada (mostrar preview, opción de mantener la existente, etc.)
                self.fields['foto'].help_text = 'Dejar en blanco para mantener la foto actual.'
                self.fields['foto'].required = False

    def clean(self):
        cleaned_data = super().clean()
        
        # Pre-procesamiento de campos para Pydantic
        sueldo_base_str = cleaned_data.get('sueldo_base')
        comision_str = cleaned_data.get('comision')

        # Normalizar strings numéricos para Pydantic (reemplazar ',' por '.' y quitar miles)
        if sueldo_base_str:
            cleaned_data['sueldo_base'] = sueldo_base_str.replace('.', '').replace(',', '.')
        if comision_str:
            cleaned_data['comision'] = comision_str.replace('.', '').replace(',', '.')
            
        try:
            # Convertir a Pydantic model
            # Excluimos foto y sueldo_bruto porque no son parte directa de la entrada Pydantic
            # y password para manejarlo antes del hashing.
            pydantic_data = {k: v for k, v in cleaned_data.items() if k not in ['foto', 'sueldo_bruto', 'password']}
            
            # Ajusta la fecha_ingreso al formato YYYY-MM-DD para Pydantic si es necesario
            if 'fecha_ingreso' in pydantic_data and pydantic_data['fecha_ingreso']:
                try:
                    # Intenta parsear la fecha de DD-MM-AAAA a YYYY-MM-DD para Pydantic
                    day, month, year = map(int, pydantic_data['fecha_ingreso'].split('-'))
                    pydantic_data['fecha_ingreso'] = f"{year:04d}-{month:02d}-{day:02d}"
                except ValueError:
                    # Si falla el parseo, Pydantic lo detectará en su field_validator
                    pass # Pydantic se encargará de la validación final

            empleado_pydantic = EmpleadoPydantic(**pydantic_data)

            # Convertir sueldo_base y comision a Decimal para Django Model
            cleaned_data['sueldo_base'] = decimal.Decimal(str(empleado_pydantic.sueldo_base))
            cleaned_data['comision'] = decimal.Decimal(str(empleado_pydantic.comision))
            # Convertir fecha_ingreso de string (validado por Pydantic) a date object
            cleaned_data['fecha_ingreso'] = empleado_pydantic.fecha_ingreso # Ya viene en YYYY-MM-DD
            
            # Hashing de la contraseña si se proporciona una nueva o se está creando
            if self.instance.pk: # Si es una actualización
                if cleaned_data.get('password'): # Si se ha introducido una nueva contraseña
                    cleaned_data['password'] = make_password(cleaned_data['password'])
                else: # Si no se ha introducido, mantener la antigua
                    cleaned_data['password'] = self.instance.password
            else: # Si es una creación
                cleaned_data['password'] = make_password(cleaned_data['password'])


        except ValidationError as e:
            for error in e.errors():
                field = error['loc'][0]
                message = error['msg']
                self.add_error(field, message) # Añade el error al campo correspondiente

        # Validar que se cargue una foto
        if 'foto' in self.cleaned_data and not self.cleaned_data['foto']:
            if not self.instance.pk or not self.instance.foto: # Si es nuevo o no tiene foto previa
                self.add_error('foto', 'Este campo es obligatorio.')

        return cleaned_data