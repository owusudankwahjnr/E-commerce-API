from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.dependency import get_db
from app.schemas.order import OrderResponse
from app.crud import order as order_crud
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order_from_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_crud.create_order_from_cart(db=db, user_id=current_user.id)


@router.get("/", response_model=List[OrderResponse])
def list_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_crud.get_orders(db=db, user_id=current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = order_crud.get_order_by_id(db=db, order_id=order_id)
    if not order or order.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return order
