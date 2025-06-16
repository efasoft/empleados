# Formulario Empleados

Este proyecto es una aplicación web desarrollada con Django para la gestión de empleados y la autenticación de usuarios. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los registros de los empleados, así como gestionar el acceso mediante un sistema de registro e inicio de sesión de usuarios.

## Características

### Gestión de Empleados (`empleados` app)
- **CRUD Completo:** Creación, visualización, actualización y eliminación de registros de empleados.
- **Eliminación Lógica (Soft Delete):** Los empleados no se eliminan permanentemente de la base de datos, sino que se marcan como inactivos.
- **Cálculo Automático de Salario:** El sueldo bruto se calcula automáticamente a partir del sueldo base y la comisión.
- **Carga de Imágenes:** Permite asociar una foto a cada empleado.
- **Paginación:** La lista de empleados está paginada para una mejor navegación.
- **Notificaciones Interactivas:** Uso de SweetAlert2 para mensajes de éxito y error más amigables.
- **Control de Acceso:** Solo los usuarios autenticados pueden gestionar empleados.

### Autenticación de Usuarios (`usuarios` app)
- **Registro de Nuevos Usuarios:** Permite a los visitantes crear una nueva cuenta.
- **Inicio de Sesión (Login):** Autenticación de usuarios existentes.
- **Cierre de Sesión (Logout):** Permite a los usuarios cerrar su sesión de forma segura.
- **Formularios Personalizados:** Utiliza formularios mejorados para el registro y el inicio de sesión.
- **Redirecciones Claras:** Guía al usuario a través del flujo de autenticación con redirecciones adecuadas.
- **Mensajes de Feedback:** Informa al usuario sobre el resultado de las acciones de autenticación.

## Tecnologías Utilizadas

- **Backend:**
  - Python 3.x
  - Django 5.0
- **Base de Datos:**
  - PostgreSQL
- **Frontend:**
  - HTML5
  - CSS3 (con Bootstrap 5 para estilos)
  - JavaScript (para interactividad y SweetAlert2)
- **Paquetes Clave de Django/Python:**
  - `django-crispy-forms` y `crispy-bootstrap5`: Para la renderización elegante de formularios.
  - `Pillow`: Para el manejo de imágenes (fotos de empleados).
  - `psycopg2-binary`: Adaptador de PostgreSQL para Python.
  - `python-dotenv`: Para la gestión de variables de entorno.
  - `email_validator`: Para la validación de correos electrónicos.

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- Python (versión 3.8 o superior recomendada)
- pip (manejador de paquetes de Python, usualmente viene con Python)
- PostgreSQL (servidor de base de datos)
- Git (para clonar el repositorio)

## Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu entorno local:

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd nombre_del_directorio_del_proyecto
    ```

2.  **Crea y activa un entorno virtual:**
    Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    Asegúrate de estar en el directorio raíz del proyecto (donde se encuentra `requirements.txt`).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    -   Crea una copia del archivo `.env.example` y renómbrala a `.env`.
        ```bash
        cp .env.example .env
        ```
    -   Abre el archivo `.env` y modifica los valores según tu configuración local, especialmente:
        -   `DJANGO_SECRET_KEY`: Genera una nueva clave secreta para tu proyecto. Puedes usar un generador online o la utilidad de Django.
        -   `DB_NAME`: El nombre de tu base de datos PostgreSQL.
        -   `DB_USER`: Tu usuario de PostgreSQL.
        -   `DB_PASSWORD`: Tu contraseña de PostgreSQL.
        -   `DB_HOST`: El host de tu servidor PostgreSQL (usualmente `localhost`).
        -   `DB_PORT`: El puerto de tu servidor PostgreSQL (usualmente `5432`).
    -   **Importante:** Asegúrate de que la base de datos especificada en `DB_NAME` exista en tu servidor PostgreSQL y que el usuario `DB_USER` tenga los permisos necesarios.

5.  **Aplica las migraciones de la base de datos:**
    Esto creará las tablas necesarias en tu base de datos.
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario (administrador):**
    Esto te permitirá acceder al panel de administración de Django y gestionar usuarios.
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones en la consola para establecer un nombre de usuario, correo electrónico y contraseña.

7.  **Recolecta los archivos estáticos (para producción o si DEBUG=False):**
    Aunque para desarrollo con `DEBUG=True` Django sirve los archivos estáticos automáticamente, es una buena práctica conocer este comando.
    ```bash
    python manage.py collectstatic
    ```

8.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/` por defecto. La página principal redirige a la lista de empleados (`/empleados/`).

## Uso

Una vez que el servidor de desarrollo esté en funcionamiento:

1.  **Página Principal:** Al acceder a `http://127.0.0.1:8000/`, serás redirigido automáticamente a la lista de empleados. Si no has iniciado sesión, serás redirigido a la página de login.

2.  **Registro de Usuarios:**
    -   Ve a `/usuarios/register/` para crear una nueva cuenta de usuario.
    -   Completa el formulario y haz clic en "Registrar".

3.  **Inicio de Sesión:**
    -   Ve a `/usuarios/login/` para acceder con tu cuenta.
    -   Ingresa tu nombre de usuario y contraseña.
    -   Al iniciar sesión correctamente, serás redirigido a la lista de empleados o a la página que intentabas acceder.

4.  **Gestión de Empleados (requiere inicio de sesión):**
    -   **Listar Empleados:** Accede a `/empleados/` para ver la lista de todos los empleados activos.
    -   **Crear Empleado:** En la lista de empleados, encontrarás un botón o enlace para "Añadir Empleado" (o similar) que te llevará al formulario de creación (`/empleados/crear/`).
    -   **Actualizar Empleado:** Desde la lista de empleados, cada registro tendrá opciones para "Editar" o "Actualizar", llevándote al formulario de edición (e.g., `/empleados/editar/<id_empleado>/`).
    -   **Eliminar Empleado (Soft Delete):** Cada empleado tendrá una opción para "Eliminar". Esto marcará al empleado como inactivo pero no lo borrará permanentemente.
    -   **Ver Detalles (si implementado):** Podría haber una opción para ver detalles completos de un empleado.

5.  **Cierre de Sesión:**
    -   Busca un enlace o botón de "Logout" o "Cerrar Sesión" (usualmente en la barra de navegación o menú de usuario) para finalizar tu sesión. Serás redirigido a la página de login.

6.  **Panel de Administración de Django:**
    -   Accede a `/admin/` e inicia sesión con las credenciales del superusuario que creaste.
    -   Desde aquí, puedes gestionar usuarios, grupos y otros modelos de Django directamente.

## Estructura del Proyecto

El proyecto sigue una estructura estándar de Django, con las siguientes aplicaciones principales:

-   `formempleados/`: Este es el directorio principal del proyecto Django.
    -   `settings.py`: Contiene la configuración principal del proyecto, como la base de datos, aplicaciones instaladas, middleware, etc.
    -   `urls.py`: Define las rutas URL principales del proyecto, delegando a las URLs de las aplicaciones.
    -   `wsgi.py` / `asgi.py`: Puntos de entrada para los servidores WSGI/ASGI.
-   `empleados/`: Aplicación Django para gestionar toda la lógica relacionada con los empleados.
    -   `models.py`: Define el modelo `Empleado` y su estructura en la base de datos.
    -   `views.py`: Contiene las vistas (basadas en clases) para las operaciones CRUD de empleados.
    -   `forms.py`: Define los formularios de Django para crear y actualizar empleados.
    -   `urls.py`: Define las rutas URL específicas para la gestión de empleados.
    -   `templates/`: Contiene las plantillas HTML para las vistas de empleados.
    -   `admin.py`: Registra el modelo `Empleado` para que sea accesible desde el panel de administración de Django.
-   `usuarios/`: Aplicación Django para gestionar la autenticación y el registro de usuarios.
    -   `views.py`: Contiene las vistas para el registro, inicio y cierre de sesión.
    -   `forms.py`: Define los formularios personalizados para el registro (`CustomUserCreationForm`) e inicio de sesión (`CustomAuthenticationForm`).
    -   `urls.py`: Define las rutas URL específicas para la autenticación de usuarios.
    -   `templates/`: Contiene las plantillas HTML para las vistas de login y registro.
-   `static/`: Directorio para archivos estáticos globales (CSS, JavaScript, imágenes) que no son específicos de una app.
-   `media/`: Directorio donde se almacenarán los archivos subidos por los usuarios (como las fotos de los empleados). *(Nota: este directorio se crea dinámicamente si no existe y se configura en `settings.py`)*.
-   `manage.py`: Utilidad de línea de comandos de Django para diversas tareas de desarrollo y administración.
-   `requirements.txt`: Lista las dependencias de Python del proyecto.
-   `.env.example` / `.env`: Archivos para gestionar variables de entorno.
-   `README.md`: Este archivo.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto:

1.  Haz un Fork del proyecto.
2.  Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Realiza tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Haz Push a la Branch (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.

Si encuentras algún error o tienes alguna sugerencia, por favor abre un "issue" en el repositorio.
