import logging
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

from database import DATABASE_FILE, get_user_by_id, get_users, update_user_status


BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "logs" / "app.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("supportlab")

app = Flask(__name__)


@app.get("/health")
def health():
    """Comprueba el estado general del servicio."""

    database_status = "available" if DATABASE_FILE.exists() else "missing"

    logger.info(
        "Health check realizado. Estado de la base: %s",
        database_status
    )

    status_code = 200 if database_status == "available" else 503

    return jsonify(
        {
            "service": "SupportLab",
            "status": "ok" if status_code == 200 else "degraded",
            "database": database_status
        }
    ), status_code

@app.get("/users")
def list_users():
    """Lista usuarios y permite filtrarlos por estado."""

    status = request.args.get("status")

    allowed_statuses = {"active", "blocked"}

    if status is not None and status not in allowed_statuses:
        logger.warning(
            "Se recibió un filtro de estado inválido: %s",
            status
        )

        return jsonify(
            {
                "error": "invalid_status",
                "received": status,
                "allowed": sorted(allowed_statuses)
            }
        ), 400

    logger.info(
        "Listando usuarios. Filtro de estado: %s",
        status if status is not None else "ninguno"
    )

    try:
        users = get_users(status)

    except sqlite3.Error:
        logger.exception(
            "Error de base de datos al listar usuarios"
        )

        return jsonify(
            {
                "error": "database_error"
            }
        ), 500

    users_as_dicts = [
        dict(user)
        for user in users
    ]

    logger.info(
        "Cantidad de usuarios encontrados: %s",
        len(users_as_dicts)
    )

    return jsonify(
        {
            "count": len(users_as_dicts),
            "users": users_as_dicts
        }
    ), 200

@app.patch("/users/<int:user_id>/status")
def change_user_status(user_id: int):
    """Modifica el estado de un usuario."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        logger.warning(
            "Solicitud sin JSON válido para usuario %s",
            user_id
        )

        return jsonify(
            {
                "error": "invalid_json"
            }
        ), 400

    status = str(data.get("status", "")).strip().lower()

    allowed_statuses = {"active", "blocked"}

    if status not in allowed_statuses:
        logger.warning(
            "Estado inválido recibido para usuario %s: %s",
            user_id,
            status
        )

        return jsonify(
            {
                "error": "invalid_status",
                "received": status,
                "allowed": sorted(allowed_statuses)
            }
        ), 400

    try:
        user = update_user_status(
            user_id=user_id,
            status=status
        )

    except sqlite3.Error:
        logger.exception(
            "Error de base de datos al modificar usuario %s",
            user_id
        )

        return jsonify(
            {
                "error": "database_error"
            }
        ), 500

    if user is None:
        logger.warning(
            "No se pudo modificar el usuario %s porque no existe",
            user_id
        )

        return jsonify(
            {
                "error": "user_not_found",
                "user_id": user_id
            }
        ), 404

    logger.info(
        "Estado del usuario %s modificado a %s",
        user_id,
        status
    )

    return jsonify(dict(user)), 200

@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    """Busca un usuario en SQLite por su ID."""

    logger.info("Buscando usuario con ID %s", user_id)

    try:
        user = get_user_by_id(user_id)

    except sqlite3.Error:
        logger.exception(
            "Error de base de datos al buscar el usuario %s",
            user_id
        )

        return jsonify(
            {
                "error": "database_error"
            }
        ), 500

    if user is None:
        logger.warning(
            "Usuario con ID %s no encontrado",
            user_id
        )

        return jsonify(
            {
                "error": "user_not_found",
                "user_id": user_id
            }
        ), 404

    logger.info(
        "Usuario con ID %s encontrado correctamente",
        user_id
    )

    return jsonify(dict(user)), 200


if __name__ == "__main__":
    logger.info("Iniciando SupportLab")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )