from app.database import db_session
from app.schemas.item import ItemSoloSchema,ItemCatalogSchema,ItemCreateSchema, ItemPatchSchema,ItemFilterSchema
from app.models import Item,Category
from sqlalchemy.orm import joinedload
from enum import Enum

class SortType(Enum):
    by_rating = "По рейтингу"
    to_increase = "Сначала дорогое"
    to_decrease = "Сначала дешевое"



def get_all_items(limit_num:int, page:int,sort_type:SortType,filters:ItemFilterSchema):
    with db_session() as session:
        items_query = session.query(Item).options(joinedload(Item.comments),
                                           joinedload(Item.images)).filter(Item.is_active == True)
        #фильтрация
        if filters.min_price:
            items_query.filter(Item.price>=filters.min_price)
        if filters.max_price:
            items_query.filter(Item.price<=filters.max_price)
        if filters.category:
            items_query.filter(Item.categories == filters.category)

        items = items_query.all()

        res_data = []
        for item in items:
            if item.comments:
                ratings = [com.rating for com in item.comments if com.rating is not None]
                if ratings:
                    rating = round(sum(ratings) / len(ratings),1)
            else:
                rating = None
            if item.images:
                try:
                    res_images = [im for im in item.images if im.is_main == True][0].url
                except:
                    res_images = None
            res_data.append(ItemCatalogSchema(id=item.id, name=item.name, images=res_images,
                                 price=item.price, rating=rating))

        # соотировка по запросу
        if sort_type == SortType.to_decrease:
            res_data.sort(key=lambda x: x.price,reverse=False)
        elif sort_type == SortType.to_increase:
            res_data.sort(key=lambda x: x.price,reverse=True)
        elif sort_type == SortType.by_rating:
            res_data.sort(key=lambda x: x.rating,reverse=True)

        res_data = res_data[(page-1)*limit_num:(page-1)*limit_num+limit_num]
        return res_data



def serv_get_item(item_id:int):
    with db_session() as session:
        item = session.query(Item).options(joinedload(Item.comments),
                                           joinedload(Item.images)).filter(Item.id ==item_id).filter(Item.is_active == True).first()
        if not item:
            raise ValueError("Item not found")
        if item.comments:
            ratings = [com.rating for com in item.comments if com.rating is not None]
            if ratings:
                rating = round(sum(ratings) / len(ratings),1)
        else:
            rating = None
        return ItemSoloSchema(id = item.id,name = item.name,images = item.images,
                              price = item.price,rating = rating,info= item.info,stock = item.stock)


def create_item(add_item:ItemCreateSchema):
    with db_session() as session:
        item = Item(**add_item.model_dump())
        session.add(item)
        session.commit()
        session.flush(item)

        return ItemSoloSchema(id = item.id,name = item.name,images = item.images,
                              price = item.price,rating = None,info= item.info,stock = item.stock)


def serv_delete_item(item_id):
    with db_session() as session:
        item = session.query(Item).filter(Item.id == item_id).filter(Item.is_active == True).first()
        if not item:
            raise ValueError("Item not found")
        item.is_active = False
        #items_in_basket = item.basket_items
        #session.delete(items_in_basket)
        return True


def serv_patch_item(item_id:int, new_data:ItemPatchSchema):
    with db_session() as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        for key,value in new_data.model_dump(exclude_none=True).items():
            setattr(item,key,value)
        session.flush()
        return ItemSoloSchema.model_validate(item)


def serv_get_categories():
    with db_session() as session:
        categories = session.query(Category).all()
        return [category.name for category in categories]



