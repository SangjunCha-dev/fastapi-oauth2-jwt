import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string(length: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string(30)}@{random_lower_string(15)}.com"


def random_password() -> str:
    return random_lower_string(32)


def random_name() -> str:
    return random_lower_string(20)


def random_age() -> int:
    return random.randint(19, 100)


def random_number() -> int:
    return random.randint(100, 10000)


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(settings.TOKEN_URL, data=login_data)
    response_json = response.json()

    access_token = response_json["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
