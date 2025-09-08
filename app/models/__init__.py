from app.models.base import Base
from app.models.user import User
from app.models.item import Item
from app.models.order import Order
from app.models.category import Category
from app.models.comment import Comment
from app.models.image import Image
from app.models.favourite import FavoriteItem
from app.models.basket_item import BasketItem
from app.models.order_item import OrderItem

#from sqlalchemy import create_engine
#from app.config import settings

#engine = create_engine(settings.DB_URL)

#Base.metadata.create_all(engine)
#Base.metadata.drop_all(engine)
