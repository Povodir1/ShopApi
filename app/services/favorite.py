from app.database import db_session
from app.models.favorite import FavoriteItem
from app.schemas.favorite import FavouriteItemSchema

def serv_add_to_favorite(user_id:int,item_id:int):
    with db_session() as session:
        existing_item = session.query(FavoriteItem).filter(FavoriteItem.user_id==user_id,
                                                           FavoriteItem.item_id==item_id).first()

        if existing_item:
            raise ValueError("Предмет уже в избранном")
        else:
            favorite_item = FavoriteItem(user_id=user_id,item_id=item_id)
            session.add(favorite_item)
        session.flush()
        if favorite_item.items.comments:
            ratings = [com.rating for com in favorite_item.items.comments if com.rating is not None]
            if ratings:
                rating = round(sum(ratings) / len(ratings),1)
        else:
            rating = None
        if favorite_item.items.images:
            try:
                res_images = [im for im in favorite_item.items.images if im.is_main == True][0].url
            except:
                res_images = None
        return FavouriteItemSchema(id = favorite_item.id,item_id = favorite_item.item_id,
                                   item_name = favorite_item.items.name,images =res_images,rating = rating)



def serv_get_favorite_items(user_id):
    with db_session() as session:
        favorite_items = session.query(FavoriteItem).filter(FavoriteItem.user_id == user_id).all()
        res_data = []
        for item in favorite_items:
            if item.items.comments:
                ratings = [com.rating for com in item.items.comments if com.rating is not None]
                if ratings:
                    rating = round(sum(ratings) / len(ratings), 1)
            else:
                rating = None
            if item.items.images:
                try:
                    res_images = [im for im in item.items.images if im.is_main == True][0].url
                except:
                    res_images = None
            res_data.append(FavouriteItemSchema(id = item.id,item_id = item.item_id,
                                                item_name = item.items.name,images =res_images,
                                                rating = rating))
        return res_data


def serv_delete_from_favorite(item_id:int,user_id:int):
    with db_session() as session:
        item = session.query(FavoriteItem).filter(FavoriteItem.user_id==user_id,
                                                  FavoriteItem.item_id==item_id).first()
        if not item:
            raise ValueError("Предмет не найден")
        session.delete(item)
        return True