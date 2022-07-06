from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=50, title="제품 이름")
    description: Optional[str] = Field(title="제품 설명")
    price: Optional[int] = Field(0, title="가격")
    quantity: Optional[int] = Field(0, title="수량")

    class Config:
        schema_extra = {
            "example": {
                "name": "제품 이름1",
                "description": "제품 설명문1",
                "price": 1000,
                "quantity": 10,
            }
        }


class ItemCreateSchema(ItemBase):
    name: str


class ItemUpdateSchema(ItemBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "제품 이름2",
                "description": "제품 설명문2",
                "price": 2000,
                "quantity": 5,
            }
        }


class ItemInDBBase(ItemBase):
    id: int = Field(..., title="제품 ID")
    name: str = Field(..., title="제품 이름")
    owner_id: int = Field(..., title="판매자 ID")

    class Config:
        orm_mode = True


class ItemSchema(ItemInDBBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "제품 이름1",
                "description": "제품 설명문1",
                "price": 1000,
                "quantity": 10,
                "id": 1,
                "owner_id": 1
            }
        }


class ItemInDB(ItemInDBBase):
    pass
