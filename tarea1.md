# Tarea: Gestor de Dispositivos IoT con SQLAlchemy y Alembic


## Objetivo

Diseñar, implementar y gestionar el esquema de una base de datos para un sistema de gestión de dispositivos IoT utilizando SQLAlchemy como ORM y Alembic para el control de versiones del esquema. Deberás definir el modelo de datos, establecer relaciones, realizar operaciones CRUD y ejecutar migraciones de base de datos.

## Contexto

Imagina que trabajas para una empresa que despliega y gestiona una flota de dispositivos IoT (sensores de temperatura, humedad, movimiento, etc.) en diversas ubicaciones. Necesitas un sistema backend para registrar estos dispositivos, los tipos de sensores que incorporan, los datos que generan, su estado operativo y cómo se agrupan lógicamente.

## Requisitos

### 1. Modelado de Datos (SQLAlchemy)

Define las siguientes clases modelo usando SQLAlchemy de acuerdo a lo visto en clases. Asegúrate de definir correctamente las claves primarias, claves foráneas y las relaciones (`relationship`) entre los modelos.

- **`TipoDispositivo`**: Representa un tipo o modelo de dispositivo (ej. 'Raspberry Pi 4', 'ESP32 Temp Sensor v2').
    - Columnas: `id` (PK, Integer), `fabricante` (String), `modelo` (String, Unique), `descripcion` (Text, Opcional).
    - Relación: Uno-a-Muchos con `Dispositivo` (un tipo puede tener muchos dispositivos).

- **`GrupoDispositivos`**: Representa una agrupación lógica de dispositivos (ej. 'Sensores Edificio A', 'Monitores Ambientales Laboratorio').
    - Columnas: `id` (PK, Integer), `nombre` (String, Unique), `descripcion` (Text, Opcional).
    - Relación: Muchos-a-Muchos con `Dispositivo`.

- **`Dispositivo`**: Representa una instancia física de un dispositivo.
    - Columnas: `id` (PK, Integer), `numero_serie` (String, Unique), `mac_address` (String, Unique, Opcional), `version_firmware` (String), `ubicacion` (String), `fecha_registro` (DateTime, default current time), `tipo_dispositivo_id` (FK a `TipoDispositivo.id`).
    - Relación: Muchos-a-Uno con `TipoDispositivo` (un dispositivo pertenece a un tipo).
    - Relación: Uno-a-Muchos con `Sensor` (un dispositivo puede tener múltiples sensores).
    - Relación: Uno-a-Muchos con `LogEstadoDispositivo` (un dispositivo tiene múltiples entradas de log).
    - Relación: Muchos-a-Muchos con `GrupoDispositivos` (un dispositivo puede pertenecer a varios grupos).

- **`Sensor`**: Representa un sensor específico dentro de un dispositivo.
    - Columnas: `id` (PK, Integer), `dispositivo_id` (FK a `Dispositivo.id`), `tipo_sensor` (String - ej. 'temperatura', 'humedad', 'movimiento'), `unidad_medida` (String - ej. '°C', '%', 'boolean').
    - Relación: Muchos-a-Uno con `Dispositivo` (un sensor pertenece a un dispositivo).
    - Relación: Uno-a-Muchos con `LecturaDato` (un sensor genera muchas lecturas).

- **`LecturaDato`**: Almacena una lectura de datos de un sensor.
    - Columnas: `id` (PK, Integer), `sensor_id` (FK a `Sensor.id`), `timestamp` (DateTime, con zona horaria, default current time), `valor_leido` (String o Float - considerar `String` para flexibilidad y parsear en la aplicación, o `Numeric` si se requiere precisión).
    - Relación: Muchos-a-Uno con `Sensor` (una lectura pertenece a un sensor).

- **`LogEstadoDispositivo`**: Registra cambios en el estado de un dispositivo.
    - Columnas: `id` (PK, Integer), `dispositivo_id` (FK a `Dispositivo.id`), `timestamp` (DateTime, default current time), `estado` (String - ej. 'online', 'offline', 'error', 'mantenimiento'), `mensaje_opcional` (Text, Opcional).
    - Relación: Muchos-a-Uno con `Dispositivo` (un log pertenece a un dispositivo).

### 2. Configuración de Alembic

- Inicializa Alembic en tu proyecto: `alembic init alembic`.
- Configura `env.py` para que utilice tus modelos de SQLAlchemy (`target_metadata = Base.metadata`) y la URL de conexión a tu base de datos. Utiliza una base de datos PostgreSQL.

### 3. Migración Inicial

- Genera la primera migración automática con Alembic basada en tus modelos definidos: `alembic revision --autogenerate -m "Initial schema"`.
- Revisa el script de migración generado en el directorio `alembic/versions/`.
- Aplica la migración para crear las tablas en la base de datos: `alembic upgrade head`.

### 4. Operaciones CRUD (SQLAlchemy)

Implementa funciones en Python (`crud.py`) que permita realizar las siguientes operaciones usando sesiones de SQLAlchemy:

- **Gestión de Tipos de Dispositivo:**
    - Añadir un nuevo `TipoDispositivo`.
    - Consultar todos los `TipoDispositivo`.
- **Gestión de Grupos de Dispositivos:**
    - Añadir un nuevo `GrupoDispositivos`.
    - Consultar todos los `GrupoDispositivos`.
- **Gestión de Dispositivos:**
    - Registrar un nuevo `Dispositivo` asociado a un `TipoDispositivo`.
    - Asociar un `Dispositivo` existente a uno o más `GrupoDispositivos`.
    - Desasociar un `Dispositivo` de un `GrupoDispositivos`.
    - Consultar todos los `Dispositivos`.
    - Consultar todos los `Dispositivos` de un `TipoDispositivo` específico.
    - Consultar todos los `Dispositivos` pertenecientes a un `GrupoDispositivos` específico.
    - Consultar los `GruposDispositivos` a los que pertenece un `Dispositivo` específico.
- **Gestión de Sensores:**
    - Añadir `Sensores` a un `Dispositivo` existente.
    - Consultar `Sensores` de un `Dispositivo`.
- **Gestión de Lecturas de Datos:**
    - Registrar una nueva `LecturaDato` para un `Sensor`.
    - Consultar las últimas N `LecturaDatos` de un `Sensor` específico.
- **Gestión de Logs de Estado:**
    - Registrar un `LogEstadoDispositivo` cuando el estado de un dispositivo cambia (simulado).
    - Consultar el historial de `LogEstadoDispositivo` para un `Dispositivo` específico.

### 5. Modificación de Esquema

Implementa las siguientes modificaciones en el esquema de la base de datos y crea una migración en Alembic para ellos:
- Modifica el modelo `Sensor`: añade una columna `umbral_alerta` (Float, nullable).
- Actualmente, para saber el estado de un dispositivo, hay que consultar el último `LogEstadoDispositivo`. Para un acceso más rápido, añade una columna `estado_actual` directamente en la tabla Dispositivo. Al añadir `estado_actual`, incluye una población inicial con el estado más reciente de `LogEstadoDispositivo` para los dispositivos existentes.
- La columna `ubicacion` en `Dispositivo` es un simple String. Modifícala para que sea más estructurada. Renombra `ubicacion` a `descripcion_ubicacion` y añade `coordenadas_gps` (String, opcional, para "lat,lon").

## Entregables

Se debe entregar un repositorio de GitHub con lo siguiente:

1. **Código Fuente Python (directorio `app/`):**
    - `models.py`: Definición de los modelos SQLAlchemy.
    - `database.py`: Configuración de la base de datos y creación de la sesión.
    - `crud.py` (o similar): Funciones para las operaciones CRUD.
    - `main.py`: Script principal para demostrar la funcionalidad (ejecución de operaciones CRUD de ejemplo).
2. **Directorio `alembic/` completo: (con todos los scripts de migración).**
3. **Archivo `pyproject.toml`, `uv.lock` y `.python-version`:**
    - Se deben incluir las dependencias necesarias para la ejecución del projecto.
4. **Archivo `README.md` con lo siguiente:**
    - Explicación breve del diseño.
    - Cómo configurar el entorno (instalación de dependencias).
    - Cómo ejecutar el código y las migraciones.
    - Estructura del proyecto.
5. **Dump de base de datos en formato SQL.**

El link del repositorio debe ser enviado por correo electrónico al mail del profesor.

## Evaluación

- **Modelado de datos (15pt)**: Correcta definición de los modelos y relaciones.
- **Migración inicial (5pt)**: Correcta configuración de Alembic y migraciones.
- **Operaciones CRUD (30pt)**: Implementación correcta de las funciones CRUD.
- **Script de prueba (10pt)**: Ejemplo funcional que demuestra el uso de las operaciones CRUD.
- **Modificaciones de esquema (10pt)**: Implementación correcta de las modificaciones solicitadas.
- **Calidad del código (10pt)**: Buenas prácticas de programación, legibilidad y uso de convenciones. Uso de tipos de datos adecuados.