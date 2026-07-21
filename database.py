import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "data" / "supportlab.db"


def get_connection() -> sqlite3.Connection:
    """Crea una conexión con la base de datos."""

    connection = sqlite3.connect(DATABASE_FILE)

    # Permite acceder a las columnas por nombre.
    connection.row_factory = sqlite3.Row

    return connection


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    """Busca un usuario por su ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, name, email, status
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()

def get_users(status: str | None = None) -> list[sqlite3.Row]:
    """Devuelve todos los usuarios o los filtra por estado."""

    connection = get_connection()

    try:
        if status is None:
            cursor = connection.execute(
                """
                SELECT id, name, email, status
                FROM users
                ORDER BY id
                """
            )

        else:
            cursor = connection.execute(
                """
                SELECT id, name, email, status
                FROM users
                WHERE status = ?
                ORDER BY id
                """,
                (status,)
            )

        return cursor.fetchall()

    finally:
        connection.close()