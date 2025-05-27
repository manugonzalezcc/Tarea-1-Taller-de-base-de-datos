# Tarea 1 - Taller de Base de Datos  
## Gestor de Dispositivos IoT con SQLAlchemy y Alembic

### Descripción

Este proyecto implementa un sistema backend para registrar y gestionar una flota de dispositivos IoT, sus sensores, lecturas y estados, utilizando **Python**, **SQLAlchemy** y **Alembic** sobre **PostgreSQL**.

---

### Estructura del Proyecto

```
Tarea 1 Taller de base de datos/
│
├── app/
│   ├── models.py         # Modelos SQLAlchemy
│   ├── crud.py           # Funciones CRUD
│   ├── database.py       # Conexión a la base de datos
│   └── main.py           # Script de pruebas
├── alembic/              # Migraciones Alembic
│   ├── env.py
│   ├── versions/
├── alembic.ini           # Configuración Alembic
├── README.md             # Este archivo
└── ...
```

---

### Requisitos

- Python 3.11+
- PostgreSQL
- Paquetes: `sqlalchemy`, `alembic`, `psycopg2-binary`

---

### Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/manugonzalezcc/Tarea-1-Taller-de-base-de-datos.git
   cd Tarea-1-Taller-de-base-de-datos
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```
   O manualmente:
   ```sh
   pip install sqlalchemy alembic psycopg2-binary
   ```

4. **Configura la base de datos:**
   - Crea una base de datos en PostgreSQL llamada `DB_tarea1_tbd`.
   - Edita `alembic.ini` y `app/database.py` con tu usuario y contraseña reales.

---

### Uso

1. **Aplica las migraciones para crear las tablas:**
   ```sh
   python -m alembic upgrade head
   ```

2. **Ejecuta el script principal para probar el sistema:**
   ```sh
   python -m app.main
   ```

   Verás en consola la creación y consulta de tipos de dispositivos, grupos, dispositivos, sensores, lecturas y logs.

---

### Notas

- Puedes modificar `app/main.py` para probar más casos o agregar tus propios datos.
- Consulta la base de datos con pgAdmin o `psql` para ver los datos insertados.

---

### Autor

Manuel González  
[GitHub](https://github.com/manugonzalezcc)

---

### Licencia

Uso académico.
