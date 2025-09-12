
from app.database import db_session
from app.schemas.item import ItemSoloSchema,ItemCatalogSchema,ItemCreateSchema
from app.schemas.image import ImageSchema
from app.models import Item,Image,Comment
from sqlalchemy.orm import joinedload



def get_all_items(limit_num:int):
    with db_session() as session:
        items = session.query(Item).options(joinedload(Item.comments),
                                           joinedload(Item.images)).limit(limit_num).all()
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
                    res_images = [ImageSchema.model_validate(im) for im in item.images if im.is_main == True][0]
                except:
                    res_images = None
            res_data.append(ItemCatalogSchema(id=item.id, name=item.name, images=res_images,
                                 price=item.price, rating=rating))
        return res_data



def get_item(item_id:int):
    with db_session() as session:
        item = session.query(Item).options(joinedload(Item.comments),
                                           joinedload(Item.images)).filter(Item.id ==item_id).first()
        if not item: return False
        if item.images:
            res_images = [ImageSchema.model_validate(im) for im in item.images]
        else:
            res_images = None
        if item.comments:
            ratings = [com.rating for com in item.comments if com.rating is not None]
            if ratings:
                rating = round(sum(ratings) / len(ratings),1)
        else:
            rating = None
        return ItemSoloSchema(id = item.id,name = item.name,images = res_images,
                              price = item.price,rating = rating,info= item.info,stock = item.stock)


def create_item(add_item:ItemCreateSchema):
    with db_session() as session:
        item = Item(**add_item.model_dump())
        session.add(item)
        session.commit()
        session.flush(item)

        return ItemSoloSchema(id = item.id,name = item.name,images = item.images,
                              price = item.price,rating = None,info= item.info,stock = item.stock)




