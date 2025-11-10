
from app.models.favorite import FavoriteItem
from app.api.favorite.schemas import FavouriteItemSchema
from app.core.exceptions import ObjectAlreadyExistError,ObjectNotFoundError

def serv_add_to_favorite(user_id:int,item_id:int,session):
    existing_item = session.query(FavoriteItem).filter(FavoriteItem.user_id==user_id,
                                                       FavoriteItem.item_id==item_id).first()

    if existing_item:
        raise ObjectAlreadyExistError("Предмет уже в избранном")
    else:
        favorite_item = FavoriteItem(user_id=user_id,item_id=item_id)
        session.add(favorite_item)
    session.flush()
    rating = None
    if favorite_item.items.comments:
        ratings = [com.rating for com in favorite_item.items.comments if com.rating is not None]
        if ratings:
            rating = round(sum(ratings) / len(ratings),1)
    res_images = None
    if favorite_item.items.images:
        res_images = [im for im in favorite_item.items.images if im.is_main == True][0].url

    return FavouriteItemSchema(id = favorite_item.id,item_id = favorite_item.item_id,
                               item_name = favorite_item.items.name,images =res_images,rating = rating)



def serv_get_favorite_items(user_id,session):
    favorite_items = session.query(FavoriteItem).filter(FavoriteItem.user_id == user_id).all()
    res_data = []
    for item in favorite_items:
        rating = None
        if item.items.comments:
            ratings = [com.rating for com in item.items.comments if com.rating is not None]
            if ratings:
                rating = round(sum(ratings) / len(ratings), 1)

        res_images = None
        if item.items.images:
            res_images = [im for im in item.items.images if im.is_main == True][0].url

        res_data.append(FavouriteItemSchema(id = item.id,item_id = item.item_id,
                                            item_name = item.items.name,images =res_images,
                                            rating = rating))
    return res_data


def serv_delete_from_favorite(item_id:int,user_id:int,session):
    item = session.query(FavoriteItem).filter(FavoriteItem.user_id==user_id,
                                              FavoriteItem.item_id==item_id).first()
    if not item:
        raise ObjectNotFoundError("Предмет не найден")
    session.delete(item)
    return True