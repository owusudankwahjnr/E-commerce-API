from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.cart import CartItemAdd, CartItemResponse, CartResponse
from app.db.dependency import get_db
from app.crud import cart as cart_crud
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])



@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = cart_crud.get_cart(db, user_id=current_user.id)
    total = sum(item.total_amount for item in cart_items)
    return CartResponse(items=cart_items, total=total)


@router.post("/add", response_model=CartItemResponse)
def add_to_cart(
    item: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = cart_crud.add_to_cart(
        db=db,
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity,
    )
    return cart_item



@router.delete("/remove", response_model=dict)
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = cart_crud.remove_from_cart(
        db=db,
        user_id=current_user.id,
        product_id=product_id,
    )
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"detail": "Item removed from cart"}
