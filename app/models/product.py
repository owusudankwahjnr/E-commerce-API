from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    cart_items = relationship("Cart", back_populates="product")
    items = relationship("OrderItem", back_populates="product")

