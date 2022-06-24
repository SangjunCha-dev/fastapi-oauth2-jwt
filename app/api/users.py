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
def read_user_me(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    현재 사용자 정보 조회
    '''
    return current_user


@router.post("/register", response_model=UserSchema)
def create_user_open(
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    name: str = Body(None),
    age: int = Body(None),
) -> Any:
    '''
    사용자 회원 가입
    '''
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(status_code=403, detail="Open user registration is forbidden on this server")
    
    user = crud_user.get_by_email(db, email=email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system")
    
    user_in = UserCreateSchema(
        email=email,
        password=password,
        name=name,
        age=age,
    )
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *, 
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdateSchema,
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    '''
    사용자 정보 수정
    '''
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="The user with this username does not exist in the system")

    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
