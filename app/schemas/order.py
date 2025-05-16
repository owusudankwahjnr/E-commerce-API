from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schemas.product import ProductResponse


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_order_time: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    product: ProductResponse

    model_config = {
        "from_attributes": True
    }


class OrderBase(BaseModel):
    total_amount: float = 0.0
    status: str = "Pending"


class OrderCreate(BaseModel):
    user_id: int


class OrderResponse(OrderBase):
    id: int
    user_id: int
    items: List[OrderItemResponse]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
