# SupportLab

SupportLab es una API REST desarrollada con Python, Flask y SQLite para practicar tareas habituales de soporte técnico de aplicaciones.

El proyecto simula un servicio de gestión de usuarios e incluye validación de solicitudes, manejo de errores, logs, monitoreo, pruebas automáticas y documentación de incidentes.

## Objetivo

El objetivo de SupportLab es demostrar habilidades aplicables a puestos como:

- Application Support Analyst
- Technical Support Engineer
- Product Support Specialist
- Junior Backend Support
- NOC / Operations Support

## Tecnologías

- Python
- Flask
- SQLite
- SQL
- Git y GitHub
- Pytest
- Requests
- API REST
- JSON
- Logging

## Funcionalidades

- Comprobar el estado del servicio y la base de datos.
- Listar todos los usuarios.
- Filtrar usuarios por estado.
- Consultar un usuario por ID.
- Crear usuarios.
- Bloquear o activar usuarios.
- Validar datos de entrada.
- Detectar emails duplicados.
- Registrar operaciones y errores en logs.
- Ejecutar pruebas automáticas.
- Monitorear la disponibilidad del servicio.
- Documentar incidentes técnicos.

## Endpoints

### Estado del servicio

```http
GET /health
```

Respuesta correcta:

```json
{
  "database": "available",
  "service": "SupportLab",
  "status": "ok"
}
```

### Listar usuarios

```http
GET /users
```

### Filtrar usuarios por estado

```http
GET /users?status=active
```

Estados permitidos:

```text
active
blocked
```

### Consultar un usuario

```http
GET /users/1
```

### Crear un usuario

```http
POST /users
Content-Type: application/json
```

Ejemplo:

```json
{
  "name": "Martín López",
  "email": "martin@example.com",
  "status": "active"
}
```

### Modificar el estado de un usuario

```http
PATCH /users/2/status
Content-Type: application/json
```

Ejemplo:

```json
{
  "status": "blocked"
}
```

## Códigos HTTP utilizados

| Código | Significado |
|---|---|
| 200 | Operación correcta |
| 201 | Recurso creado |
| 400 | Solicitud inválida |
| 404 | Recurso no encontrado |
| 405 | Método HTTP no permitido |
| 409 | Conflicto por datos duplicados |
| 500 | Error interno del servidor |
| 503 | Servicio no disponible |

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/sebastianmaldonado1991-spec/supportlab.git
cd supportlab
```

Crear y activar el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Inicializar la base de datos

```bash
python init_db.py
```

Este comando crea la base SQLite e inserta los usuarios iniciales.

## Ejecutar la aplicación

```bash
python app.py
```

La API estará disponible en:

```text
http://127.0.0.1:5000
```

## Ejemplos con curl

Comprobar el servicio:

```bash
curl -i http://127.0.0.1:5000/health
```

Consultar usuarios:

```bash
curl -i http://127.0.0.1:5000/users
```

Crear un usuario:

```bash
curl -i -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{
  "name": "Martín López",
  "email": "martin@example.com",
  "status": "active"
}'
```

Modificar el estado:

```bash
curl -i -X PATCH http://127.0.0.1:5000/users/2/status \
-H "Content-Type: application/json" \
-d '{
  "status": "blocked"
}'
```

## Pruebas automáticas

Ejecutar todas las pruebas:

```bash
python -m pytest -v
```

Las pruebas comprueban:

- estado del servicio;
- consulta de usuarios;
- usuarios inexistentes;
- filtros por estado;
- creación de usuarios;
- emails duplicados;
- modificación de estados;
- validación de solicitudes.

## Monitor del servicio

Con la API ejecutándose:

```bash
python monitor.py
```

Respuesta saludable:

```text
OK: SupportLab está saludable | database=available
```

Si la aplicación está apagada o no responde:

```text
CRITICAL: No fue posible conectarse con SupportLab
```

El monitor devuelve:

- código de salida `0` cuando el servicio está saludable;
- código de salida `1` cuando detecta un problema.

## Logs

La aplicación registra actividad y errores en:

```text
logs/app.log
```

Para observar el log en tiempo real:

```bash
tail -f logs/app.log
```

Para buscar errores:

```bash
grep "ERROR" logs/app.log
```

## Incidentes documentados

Los ejercicios de diagnóstico y recuperación están documentados en la carpeta:

```text
incidents/
```

### INC-001 — Base de datos no disponible

En este incidente se practicó:

1. detección mediante `/health`;
2. análisis del código HTTP;
3. revisión de logs;
4. identificación de la causa raíz;
5. restauración de la base;
6. verificación de la recuperación;
7. propuesta de medidas preventivas.

## Estructura del proyecto

```text
supportlab/
├── data/
├── incidents/
├── logs/
├── tests/
│   └── test_api.py
├── app.py
├── database.py
├── init_db.py
├── monitor.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Habilidades demostradas

- Diagnóstico de aplicaciones.
- Interpretación de códigos HTTP.
- Consumo y desarrollo de APIs REST.
- Consultas SQL.
- Manejo de errores.
- Lectura y generación de logs.
- Automatización con Python.
- Monitoreo de servicios.
- Pruebas automatizadas.
- Documentación de incidentes.
- Control de versiones con Git.