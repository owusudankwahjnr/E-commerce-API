from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import root, auth, product, cart, order
from app.models import user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)