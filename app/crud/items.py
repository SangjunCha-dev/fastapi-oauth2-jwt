from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.items import ItemModel
from app.schemas.items import *


class CRUDItem(CRUDBase[ItemModel, ItemCreateSchema, ItemUpdateSchema]):
    def create_with_owner(self, db: Session, *, obj_in: ItemCreateSchema, owner_id: int) -> ItemModel:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> list[ItemModel]:
        return (
            db.query(self.model)
            .filter(ItemModel.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_user_item(db: Session, item: ItemCreateSchema, user_id: int):
        db_item = ItemModel(
            **item.dict(),
            owner_id=user_id,
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

crud_item = CRUDItem(ItemModel)
