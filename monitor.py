import sys

import requests


HEALTH_URL = "http://127.0.0.1:5000/health"
TIMEOUT_SECONDS = 5


def check_service() -> bool:
    """Consulta el estado de SupportLab."""

    try:
        response = requests.get(
            HEALTH_URL,
            timeout=TIMEOUT_SECONDS
        )

    except requests.ConnectionError:
        print("CRITICAL: No fue posible conectarse con SupportLab")
        return False

    except requests.Timeout:
        print(
            f"CRITICAL: SupportLab no respondió "
            f"en {TIMEOUT_SECONDS} segundos"
        )
        return False

    except requests.RequestException as error:
        print(f"CRITICAL: Error inesperado: {error}")
        return False

    try:
        data = response.json()

    except ValueError:
        print("CRITICAL: La respuesta no contiene JSON válido")
        return False

    if response.status_code == 200 and data.get("status") == "ok":
        print(
            "OK: SupportLab está saludable "
            f"| database={data.get('database')}"
        )
        return True

    print(
        "CRITICAL: SupportLab presenta problemas "
        f"| http_status={response.status_code} "
        f"| status={data.get('status')} "
        f"| database={data.get('database')}"
    )

    return False


if __name__ == "__main__":
    service_is_healthy = check_service()

    if service_is_healthy:
        sys.exit(0)

    sys.exit(1)