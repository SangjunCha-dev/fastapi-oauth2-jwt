from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.depends import get_current_active_user
from app.crud.items import crud_item
from app.crud.users import crud_user
from app.models.users import UserModel
from app.schemas.items import *

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=200, response_model=list[ItemSchema])
def get_items(
    db: Session = Depends(get_db),
    skip: int = 0, 
    limit: int = 100, 
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    제품 목록 조회
    '''
    if crud_user.is_superuser(current_user):
        items = crud_item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud_item.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)

    return items


@router.get("/{id}", status_code=200, response_model=ItemSchema)
def get_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    제품 정보 조회
    '''
    item = crud_item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return item


@router.post("", status_code=201, response_model=ItemSchema)
def create_item(
    *, 
    db: Session = Depends(get_db),
    item_in: ItemCreateSchema,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    제품 정보 등록
    '''
    item = crud_item.create_with_owner(db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{id}", status_code=200, response_model=ItemSchema)
def update_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    item_in: ItemUpdateSchema,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    제품 정보 수정
    '''
    item = crud_item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    item = crud_item.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{id}", status_code=200, response_model=ItemSchema)
def delete_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    '''
    제품 정보 삭제
    '''
    item = crud_item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    item = crud_item.remove(db, id=id)
    return item
