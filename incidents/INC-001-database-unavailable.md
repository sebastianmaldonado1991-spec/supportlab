# INC-001 — Base de datos no disponible

## Resumen

La API SupportLab dejó de responder correctamente a las consultas de usuarios porque el archivo de base de datos SQLite no estaba disponible.

## Impacto

- El endpoint `/health` respondió `503 Service Unavailable`.
- El endpoint `/users` respondió `500 Internal Server Error`.
- No fue posible consultar usuarios durante el incidente.

## Detección

El problema fue detectado mediante:

- Consulta al endpoint `/health`.
- Código HTTP 503.
- Revisión del archivo `logs/app.log`.
- Error SQLite relacionado con la ausencia de la tabla `users`.

## Causa raíz

El archivo `data/supportlab.db` había sido movido o no estaba disponible.

Al intentar realizar una consulta, SQLite creó una base vacía que no contenía la tabla `users`.

## Resolución

1. Se detuvo la aplicación.
2. Se eliminó la base vacía creada automáticamente.
3. Se restauró el archivo original `supportlab.db`.
4. Se reinició Flask.
5. Se verificaron `/health` y `/users`.

## Verificación

Después de restaurar la base:

- `/health` respondió `200 OK`.
- `/users` respondió `200 OK`.
- Los usuarios volvieron a estar disponibles.

## Prevención propuesta

- Mejorar la comprobación del endpoint `/health`.
- Verificar no solo la existencia del archivo, sino también la conexión y la tabla `users`.
- Crear un script de monitoreo automático.
- Implementar copias de seguridad de la base de datos.