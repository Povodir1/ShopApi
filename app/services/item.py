from app.database import db_session
from app.schemas.item import ItemSoloSchema,ItemCatalogSchema,ItemCreateSchema, ItemPatchSchema
from app.models import Item,Category
from sqlalchemy.orm import joinedload



def get_all_items(limit_num:int):
    with db_session() as session:
        items = session.query(Item).options(joinedload(Item.comments),
                                           joinedload(Item.images)).filter(Item.is_active == True).limit(limit_num).all()
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
                    res_images = [im for im in item.images if im.is_main == True][0]
                except:
                    res_images = None
            res_data.append(ItemCatalogSchema(id=item.id, name=item.name, images=res_images,
                                 price=item.price, rating=rating))
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



