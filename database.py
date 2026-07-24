import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "data" / "supportlab.db"


def get_connection() -> sqlite3.Connection:
    """Crea una conexión con la base de datos."""

    if not DATABASE_FILE.exists():
        raise sqlite3.OperationalError(
            f"No se encontró la base de datos: {DATABASE_FILE}"
        )

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    return connection

def update_user_status(user_id: int, status: str):
    """Modifica el estado de un usuario y devuelve sus datos."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE users
            SET status = ?
            WHERE id = ?
            """,
            (status, user_id)
        )

        # Si no modificó ninguna fila, el usuario no existe.
        if cursor.rowcount == 0:
            return None

        connection.commit()

        user = connection.execute(
            """
            SELECT id, name, email, status
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        return user

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

def check_database() -> None:
    """Comprueba la conexión y la existencia de la tabla users."""

    connection = get_connection()

    try:
        connection.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        ).fetchone()

    finally:
        connection.close()


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

def create_user(
    name: str,
    email: str,
    status: str = "active"
) -> sqlite3.Row:
    """Crea un usuario en la base y devuelve sus datos."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (name, email, status)
            VALUES (?, ?, ?)
            """,
            (name, email, status)
        )

        connection.commit()

        user = connection.execute(
            """
            SELECT id, name, email, status
            FROM users
            WHERE id = ?
            """,
            (cursor.lastrowid,)
        ).fetchone()

        if user is None:
            raise sqlite3.DatabaseError(
                "El usuario se insertó, pero no pudo recuperarse"
            )

        return user

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()

