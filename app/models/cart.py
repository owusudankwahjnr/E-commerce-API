from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)  # Quantity of the product in the cart

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    @property
    def total_amount(self) -> float:
        if self.product:
            return self.quantity * self.product.price
        return 0.0
