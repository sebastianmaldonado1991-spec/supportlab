import json
import logging
from pathlib import Path

from flask import Flask, jsonify


# Ruta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent

USERS_FILE = BASE_DIR / "data" / "users.json"
LOG_FILE = BASE_DIR / "logs" / "app.log"


# Configuración de logs
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


def load_users() -> list[dict]:
    """Carga los usuarios desde el archivo JSON."""

    with USERS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/health")
def health():
    """Comprueba si la aplicación está funcionando."""

    logger.info("Health check realizado correctamente")

    return jsonify(
        {
            "service": "SupportLab",
            "status": "ok"
        }
    ), 200


@app.get("/users/<int:user_id>")
def get_user(user_id: int):
    """Busca un usuario por su ID."""

    logger.info("Buscando usuario con ID %s", user_id)

    try:
        users = load_users()

    except FileNotFoundError:
        logger.exception("No se encontró el archivo de usuarios")

        return jsonify(
            {
                "error": "users_file_not_found"
            }
        ), 500

    except json.JSONDecodeError:
        logger.exception("El archivo de usuarios contiene JSON inválido")

        return jsonify(
            {
                "error": "invalid_users_file"
            }
        ), 500

    user = next(
        (item for item in users if item["id"] == user_id),
        None
    )

    if user is None:
        logger.warning("Usuario con ID %s no encontrado", user_id)

        return jsonify(
            {
                "error": "user_not_found",
                "user_id": user_id
            }
        ), 404

    logger.info("Usuario con ID %s encontrado correctamente", user_id)

    return jsonify(user), 200


if __name__ == "__main__":
    logger.info("Iniciando SupportLab")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )