from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.cart import Cart
from app.models.product import Product


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity. Must be greater than zero.")

    # Check product existence
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if cart item already exists
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity = quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart(db: Session, user_id: int):
    # Include related product data for response
    cart_items = db.query(Cart).options(joinedload(Cart.product)).filter(
        Cart.user_id == user_id
    ).all()

    return cart_items


def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return True
