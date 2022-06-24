from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.users import UserModel
from app.schemas.users import UserCreateSchema, UserUpdateSchema
from app.crud.users import crud_user
from app.tests.utils.utils import *


def user_authentication_headers(
    *,
    client: TestClient,
    email: str, 
    password: str,
) -> dict[str, str]:
    login_data = {
        "username": email,
        "password": password,
    }

    response = client.post(settings.TOKEN_URL, data=login_data)
    response_json = response.json()
    
    access_token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def create_random_user(db: Session) -> UserModel:
    user_in = UserCreateSchema(
        email=random_email(),
        password=random_password(),
        name=random_name(),
        age=random_age(),
    )

    return crud_user.create(db, obj_in=user_in)


def authentication_token_from_email(
    db: Session,
    client: TestClient,
    email: str,
) -> dict[str, str]:
    '''
    Returns valid access_token from the email user

    user creation if user is not exist
    '''
    password = random_password()
    user = crud_user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreateSchema(
            email=email,
            password=password,
            name=random_name(),
            age=random_age(),
        )

        user = crud_user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdateSchema(password=password)
        user = crud_user.update(db, db_obj=user, obj_in=user_in_update)
    
    return user_authentication_headers(client=client, email=email, password=password)
