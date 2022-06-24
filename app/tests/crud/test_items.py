from sqlalchemy.orm import Session

from app.crud.items import crud_item
from app.schemas.items import ItemCreateSchema, ItemUpdateSchema
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string, random_name, random_number


def test_create_item(db: Session) -> None:
    name=random_name()
    description=random_lower_string(100)
    price=random_number()
    quantity=random_number()

    item_in = ItemCreateSchema(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    user = create_random_user(db)

    item = crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)

    assert item.name == name
    assert item.description == description
    assert item.price == price
    assert item.quantity == quantity
    assert item.owner_id == user.id


def test_get_item(db: Session) -> None:
    name=random_name()
    description=random_lower_string(100)
    price=random_number()
    quantity=random_number()

    item_in = ItemCreateSchema(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    user = create_random_user(db)
    item = crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)

    get_item = crud_item.get(db=db, id=item.id)

    assert get_item
    assert get_item.id == item.id
    assert get_item.name == name
    assert get_item.description == description
    assert get_item.price == price
    assert get_item.quantity == quantity
    assert get_item.owner_id == user.id


def test_update_item(db: Session) -> None:
    name=random_name()
    description=random_lower_string(100)
    price=random_number()
    quantity=random_number()

    item_in = ItemCreateSchema(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    user = create_random_user(db)
    item = crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)

    new_name=random_name()
    new_description = random_lower_string(100)
    new_price=random_number()
    new_quantity=random_number()

    item_update = ItemUpdateSchema(
        name=new_name,
        description=new_description,
        price=new_price,
        quantity=new_quantity,
    )
    updated_item = crud_item.update(db=db, db_obj=item, obj_in=item_update)

    assert updated_item.id == item.id
    assert updated_item.name == new_name
    assert updated_item.description == new_description
    assert updated_item.price == new_price
    assert updated_item.quantity == new_quantity
    assert updated_item.owner_id == user.id


def test_delete_item(db: Session) -> None:
    name=random_name()
    description=random_lower_string(100)
    price=random_number()
    quantity=random_number()

    item_in = ItemCreateSchema(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    user = create_random_user(db)
    item = crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)

    deleted_item = crud_item.remove(db=db, id=item.id)
    get_item = crud_item.get(db=db, id=item.id)

    assert get_item is None
    assert deleted_item.id == item.id
    assert deleted_item.name == name
    assert deleted_item.description == description
    assert deleted_item.owner_id == user.id
