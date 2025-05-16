from sqlalchemy import Column, Integer, ForeignKey, Float, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

from app.db.database import Base

class OrderStatus(str, enum.Enum):
    pending = "Pending"
    completed = "Completed"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, default=0)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)  # Price at the time of order

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
