"""   Creado por IA """

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator, field_validator 
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
            # También maneja formatos con guiones o barras y convierte a YYYY-MM-DD
            day, month, year = map(int, value.replace('/', '-').split('-'))
            parsed_date = date(year, month, day)
            return parsed_date.strftime('%Y-%m-%d') # Retorna en formato YYYY-MM-DD para la base de datos
        except ValueError:
            raise ValueError("La fecha debe estar en formato DD-MM-AAAA.")

    @field_validator('sueldo_base', 'comision')
    @classmethod
    def validate_numeric_format(cls, value):
        # Para manejar "1.234,56" o "1,234.56" o "1234.56"
        # Primero, asegúrate de que el valor sea un string antes de manipularlo
        value_str = str(value)
        # Quita separadores de miles (punto o coma) y cambia coma decimal por punto
        cleaned_value = value_str.replace('.', '').replace(',', '.')
        try:
            return float(cleaned_value)
        except ValueError:
            raise ValueError("El sueldo o comisión debe tener un formato numérico válido.")

    @model_validator(mode='after')
    def validate_amounts_positive(self):
        # Validar que los sueldos y comisiones sean positivos después de que se hayan convertido a float
        if self.sueldo_base < 0:
            raise ValueError("Sueldo Base debe ser un número positivo.")
        if self.comision < 0:
            raise ValueError("Comisión debe ser un número positivo.")
        return self # Importante retornar self en model_validator(mode='after')

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