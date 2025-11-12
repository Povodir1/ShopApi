from sqlalchemy.orm import joinedload

from app.models import BasketItem,Item
from app.models.user import CurrencyType

from app.api.basket.schemas import BasketItemSchema,BasketSchema

from app.core.exceptions import ObjectNotFoundError

from app.utils.currency_tools import convert_currency



def serv_add_to_basket(user_id:int,item_id:int,count:int,currency_type:CurrencyType ,session):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise ObjectNotFoundError("Предмет не найден")

    existing_item = session.query(BasketItem).filter(BasketItem.user_id==user_id,
                                                     BasketItem.item_id==item_id).first()

    if existing_item:
        existing_item.count += count
        basket_item = existing_item
    else:
        basket_item = BasketItem(user_id=user_id,item_id=item_id,count=count)
        session.add(basket_item)
    session.flush()
    rating = None
    if basket_item.items.comments:
        ratings = [com.rating for com in basket_item.items.comments if com.rating is not None]
        if ratings:
            rating = round(sum(ratings) / len(ratings),1)

    if basket_item.items.images:
        res_images = [im for im in basket_item.items.images if im.is_main == True][0].url
        if not res_images:
            res_images = None
    else:
        res_images = None
    return BasketItemSchema(id = basket_item.id,item_id = basket_item.item_id,
                            item_name = basket_item.items.name,images =res_images,
                            count = basket_item.count,
                            full_price = convert_currency(CurrencyType.USD,currency_type,basket_item.count*basket_item.items.price),
                            rating = rating)

def serv_get_basket_items(user_id:int,currency_type:CurrencyType,session):
    basket_items = session.query(BasketItem).options(
    joinedload(BasketItem.items)).filter(BasketItem.user_id == user_id).all()
    res_data = []
    for item in basket_items:
        rating = None
        if item.items.comments:
            ratings = [com.rating for com in item.items.comments if com.rating is not None]
            if ratings:
                rating = round(sum(ratings) / len(ratings), 1)
        if item.items.images:
            res_images = [im for im in item.items.images if im.is_main == True][0].url
            if not res_images:
                res_images = None
        else:
            res_images = None
        res_data.append(BasketItemSchema(id = item.id,item_id = item.item_id,item_name = item.items.name,
                                         images =res_images,count = item.count,
                                         full_price = convert_currency(CurrencyType.USD,currency_type,item.count*item.items.price),rating = rating))
    return BasketSchema(items=res_data,item_count= len(res_data),full_price= convert_currency(CurrencyType.USD,currency_type,sum([i.full_price for i in res_data])))


def serv_delete_from_basket(item_id:int,user_id:int,session):
    item = session.query(BasketItem).filter(BasketItem.user_id==user_id,
                                            BasketItem.item_id==item_id).first()
    if not item:
        raise ObjectNotFoundError("Предмет не найден")
    session.delete(item)







