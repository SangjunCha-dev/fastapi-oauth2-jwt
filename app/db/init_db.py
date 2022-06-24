from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.users import crud_user
from app.schemas.users import UserCreateSchema


def init_db(db: Session) -> None:
    '''
    관리자 계정 생성
    '''
    if not crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL):
        user_in = UserCreateSchema(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud_user.create(db, obj_in=user_in)
