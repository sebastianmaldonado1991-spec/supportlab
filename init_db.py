import sqlite3

from database import DATABASE_FILE


USERS = [
    (1, "Ana Torres", "ana@example.com", "active"),
    (2, "Carlos Gómez", "carlos@example.com", "blocked"),
    (3, "Lucía Pérez", "lucia@example.com", "active")
]


def initialize_database() -> None:
    """Crea la base de datos y carga usuarios de prueba."""

    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute("DROP TABLE IF EXISTS users")

        connection.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL
                    CHECK(status IN ('active', 'blocked'))
            )
            """
        )

        connection.executemany(
            """
            INSERT INTO users (id, name, email, status)
            VALUES (?, ?, ?, ?)
            """,
            USERS
        )

        connection.commit()

        print(f"Base de datos creada en: {DATABASE_FILE}")
        print(f"Usuarios insertados: {len(USERS)}")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()