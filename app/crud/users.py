from typing import Union, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.core.security import get_password_hash, verify_password
from app.models.users import UserModel
from app.schemas.users import *


class CRUDUser(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):  
    def create(self, db: Session, *, obj_in: UserCreateSchema) -> UserModel:
        if not hasattr(obj_in, "is_active"):
            obj_in.is_active = True

        db_obj = UserModel(
            name=obj_in.name,
            email=obj_in.email,
            age=obj_in.age,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: UserModel, obj_in: Union[UserUpdateSchema, dict[str, Any]]) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserModel]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser


crud_user = CRUDUser(UserModel)
