from typing import Optional

from sqlalchemy.orm import Session

from app.models.items import ItemModel
from app.schemas.items import ItemCreateSchema
from app.crud.items import crud_item
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string, random_name, random_number


def create_random_item(
    db: Session,
    owner_id: Optional[int] = None,
) -> ItemModel:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    
    item_in = ItemCreateSchema(
        name=random_name(),
        description=random_lower_string(100),
        price=random_number(),
        quantity=random_number(),
    )
    return crud_item.create_with_owner(db, obj_in=item_in, owner_id=owner_id)