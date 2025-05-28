# No se necesita un modelo de usuario personalizado si usamos el User de Django.
# Si hubieras querido extenderlo con más campos, lo harías aquí.
# Para este proyecto, el prompt indica usar el User de Django, por lo que este archivo puede quedar vacío
# o contener un modelo que herede de AbstractUser si se necesita.
# Dejamos vacío o con un placeholder para dejar claro que no se requiere un modelo adicional aquí
# si solo usamos las funciones de autenticación base.

# from django.contrib.auth.models import AbstractUser
#
# class CustomUser(AbstractUser):
#     # Añade campos personalizados aquí si es necesario
#     # Por ejemplo:
#     # date_of_birth = models.DateField(null=True, blank=True)
#     pass
