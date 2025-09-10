from requests import Session

from app.database import db_session
from app.schemas.item import ItemSoloSchema
from app.schemas.image import ImageSchema
from app.models import Item,Image,Comment
from sqlalchemy.orm import joinedload


#добавить пагинацию
def get_all_items():
    pass


#доделать рейтинг
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


