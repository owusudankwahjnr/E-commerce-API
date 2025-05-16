from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from datetime import datetime


def create_order_from_cart(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for '{product.name}'")

        # Reduce product stock
        product.stock -= item.quantity

        # Compute subtotal
        subtotal = product.price * item.quantity
        total_amount += subtotal

        # Prepare order item
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order_time=product.price
        )
        order_items.append(order_item)

    # Create order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="Pending",
        created_at=datetime.utcnow(),
        items=order_items
    )

    db.add(order)

    # Clear cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()

    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, user_id: int):
    return db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.user_id == user_id).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product))\
        .filter(Order.id == order_id).first()
