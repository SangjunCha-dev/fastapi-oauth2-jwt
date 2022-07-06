from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.config import settings
from app.core.depends import get_current_user
from app.db.database import get_db
from app.crud.users import crud_user
from app.models.users import UserModel
from app.schemas.token import TokenSchema
from app.schemas.users import UserSchema

router = APIRouter(
    prefix="/login",
    tags=["login"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/access-token", status_code=201, response_model=TokenSchema)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    '''
    OAuth2 호환 토큰 로그인
    '''
    user = crud_user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            user.id, 
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", status_code=201, response_model=UserSchema)
def test_token(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    '''
    access token 테스트
    '''
    return current_user
