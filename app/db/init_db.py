from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.users import crud_user
from app.schemas.users import UserCreateSchema


def init_db(db: Session) -> None:
    '''
    테스트 계정 생성
    '''
    # 테스트 관리자 계정 생성
    if not crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL):
        user_in = UserCreateSchema(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud_user.create(db, obj_in=user_in)

    # 테스트 계정 생성
    if not crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL):
        user_in = UserCreateSchema(
            email=settings.TEST_USER_EMAIL,
            password=settings.TEST_USER_PASSWORD,
            is_superuser=False,
        )
        crud_user.create(db, obj_in=user_in)
