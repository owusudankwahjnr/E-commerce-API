from pydantic import BaseModel, field_validator
from typing import List, Optional

from app.schemas.product import ProductResponse


class CartItemBase(BaseModel):
    id: int
    user_id: int
    quantity: Optional[int] = 1  # Default to 1 if no quantity is provided

    @field_validator('quantity')
    def check_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('"Invalid quantity. Must be greater than zero."')
        return value



class CartItemCreate(CartItemBase):
    product_id: int

class CartItemUpdate(CartItemBase):
    product_id: int

class CartItemAdd(CartItemBase):
    product_id: int


class CartItemResponse(CartItemBase):

    product: ProductResponse
    total_amount: float

    model_config = {
        "from_attributes": True
    }

class CartResponse(BaseModel):

    items: List[CartItemResponse]
    total: float

    model_config = {
        "from_attributes": True
    }
