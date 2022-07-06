from typing import Any

from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.depends import get_current_active_user, get_current_active_superuser
from app.core.config import settings
from app.crud.users import crud_user
from app.models.users import UserModel
from app.schemas.users import *
from app.schemas.items import *

router = APIRouter(
    prefix="/users",
    tags=['users'],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.get("/me", response_model=UserSchema)
def get_user_me(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    현재 사용자 정보 조회
    '''
    return current_user


@router.post("", response_model=UserSchema)
def create_user_public(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreateSchema,
) -> Any:
    '''
    사용자 회원 가입
    '''
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(status_code=403, detail="Open user registration is forbidden on this server")
    
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system")

    user = crud_user.create(db, obj_in=user_in)
    return user


@router.put("", response_model=UserSchema)
def update_user(
    *, 
    db: Session = Depends(get_db),
    user_in: UserUpdateSchema,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    사용자 정보 수정
    '''
    user = crud_user.get(db, id=current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="The user with this email does not exist in the system")

    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
