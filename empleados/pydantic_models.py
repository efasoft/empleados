"""   Creado por IA """

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
import re

class EmpleadoPydantic(BaseModel):
    nombres: str = Field(..., max_length=60, min_length=1)
    apellidos: str = Field(..., max_length=60, min_length=1)
    edad: int = Field(..., gt=0, le=100)
    fecha_ingreso: str # Se valida como string y luego se parsea
    email: EmailStr
    telefono_casa: Optional[str] = Field(None, pattern=r"^\+?34[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}[ -]?\d{2}$") # Formato de teléfono fijo España
    telefono_movil: str = Field(..., pattern=r"^\+?34[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}$") # Formato de teléfono móvil España
    sueldo_base: float
    comision: float
    # sueldo_bruto no se incluye aquí porque se calcula en el modelo Django, no se espera como entrada directa
    password: str = Field(..., min_length=8)
    # foto no se valida directamente aquí porque Django maneja el Field de archivo

    @field_validator('fecha_ingreso')
    @classmethod
    def validate_fecha_ingreso(cls, value):
        try:
            # Intenta parsear la fecha en formato DD-MM-AAAA
            parsed_date = date.fromisoformat(value.replace('/', '-').replace('.', '-')) # Permite /, . o -
            return parsed_date.strftime('%Y-%m-%d') # Retorna en formato YYYY-MM-DD para la base de datos
        except ValueError:
            # Intenta parsear con un formato alternativo si el primero falla
            try:
                day, month, year = map(int, value.split('-'))
                parsed_date = date(year, month, day)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError("La fecha debe estar en formato DD-MM-AAAA.")

    @model_validator(mode='after')
    def validate_sueldo_format(self):
        # Esta validación es más compleja con Pydantic directamente para el formato
        # Si se espera que los números vengan con separadores de miles/decimales,
        # Pydantic los parseará a float directamente. Si necesitas validar la *entrada*
        # del string antes de la conversión a float, tendrías que recibirlo como str
        # y luego validarlo con regex antes de convertirlo.
        # Para simplificar y dado que Django y PostgreSQL manejan DecimalField,
        # Pydantic lo validará como float por defecto.
        # Asumimos que los valores se pasarán como números flotantes.
        if not isinstance(self.sueldo_base, (float, int)) or self.sueldo_base < 0:
            raise ValueError("Sueldo Base debe ser un número positivo.")
        if not isinstance(self.comision, (float, int)) or self.comision < 0:
            raise ValueError("Comisión debe ser un número positivo.")
        return self

    @field_validator('sueldo_base', 'comision')
    @classmethod
    def validate_numeric_format(cls, value):
        # Pydantic convertirá automáticamente a float si el tipo es float.
        # Si la entrada fuera un string como "1.234,56", tendríamos que
        # procesarla antes de que Pydantic intente convertirla a float.
        # Aquí asumimos que la entrada ya es un número o un string parseable a float.
        # Si se quiere validar específicamente el string de entrada con formato de miles/decimales
        # (ej. "1.234,56" para español), el campo en Pydantic debería ser 'str'
        # y la validación custom. Para DecimalField de Django, se espera un float/Decimal.
        # Si el input del formulario se maneja como string y luego se convierte,
        # la validación de formato puede ser en el formulario de Django.
        # Para Pydantic, un float es un float.
        try:
            return float(str(value).replace('.', '').replace(',', '.')) # Para manejar "1.234,56" o "1,234.56"
        except ValueError:
            raise ValueError("El sueldo o comisión debe tener un formato numérico válido.")

    class Config:
        json_schema_extra = {
            "example": {
                "nombres": "Juan",
                "apellidos": "Perez",
                "edad": 30,
                "fecha_ingreso": "15-03-2023",
                "email": "juan.perez@example.com",
                "telefono_casa": "+34 912 34 56 78",
                "telefono_movil": "+34 600 111 222",
                "sueldo_base": 2500.50,
                "comision": 150.75,
                "password": "MiPasswordSeguro123",
            }
        }