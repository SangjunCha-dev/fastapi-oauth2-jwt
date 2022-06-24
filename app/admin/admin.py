from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.depends import get_current_active_user, get_current_active_superuser
from app.crud.users import crud_user
from app.models.users import *
from app.schemas.users import *

router = APIRouter(
    prefix="/admin",
    tags=['admin'],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.get("/users", response_model=list[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 100, 
    current_user: UserModel = Depends(get_current_active_superuser),
):
    '''
    사용자 목록 조회(관리자 권한)
    '''
    return crud_user.get_multi(db, skip=skip, limit=limit)


@router.post("/users", response_model=UserSchema)
def add_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreateSchema,
    current_user: UserModel = Depends(get_current_active_superuser),
):
    '''
    사용자 추가(관리자 권한)
    '''
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.get("/users/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    '''
    user_id 사용자 정보 조회(관리자 권한)
    '''
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user
