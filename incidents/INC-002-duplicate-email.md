# INC-002 — Intento de crear un usuario con email duplicado

## Resumen

Se intentó crear un usuario utilizando un email que ya estaba registrado en SupportLab.

## Impacto

La solicitud fue rechazada y el segundo usuario no fue creado.

La API continuó funcionando normalmente y los datos existentes no fueron modificados.

## Detección

El incidente fue detectado mediante:

- respuesta HTTP `409 Conflict`;
- mensaje `email_already_exists`;
- revisión de `logs/app.log`;
- consulta directa a la base SQLite.

## Causa raíz

La columna `email` de la tabla `users` posee una restricción `UNIQUE`.

SQLite rechazó el segundo `INSERT` porque el email ya existía y generó una excepción `sqlite3.IntegrityError`.

## Resolución

La aplicación capturó la excepción y devolvió una respuesta controlada:

- código HTTP `409`;
- descripción del conflicto;
- email involucrado.

No fue necesario reiniciar el servicio ni modificar la base.

## Verificación

Se ejecutó una consulta SQL para confirmar que existía solamente una fila con el email involucrado.

También se ejecutaron las pruebas automáticas y todas finalizaron correctamente.

## Prevención

- Mantener la restricción `UNIQUE` en la base.
- Validar y normalizar emails antes de insertarlos.
- Conservar una prueba automática para emails duplicados.
- Registrar el conflicto en los logs sin exponer información sensible.