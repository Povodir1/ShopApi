# Сначала импортируем все модели
from base import Base
from user import User
from item import Item
from order import Order
from category import Category
from comment import Comment
from image import Image
from favourite import FavoriteItem
from basket_item import BasketItem
from order_item import OrderItem

# Создание таблицы в базе данных
#engine = create_engine(settings.DB_URL)
#Base.metadata.create_all(engine)
#Base.metadata.drop_all(engine)
