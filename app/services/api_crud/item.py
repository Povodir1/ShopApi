import datetime


from app.schemas.item import ItemSoloSchema,ItemCatalogSchema,ItemCreateSchema, ItemPatchSchema,ItemFilterSchema,AttributeData,CatalogSchema
from app.models import Item, Category, Image, User, Attribute, AttributeValue, Tag,ItemTag
from app.services.preference_logic import update_user_preference
from app.services.utils.currency_tools import convert_currency
from app.models.user import CurrencyType
from sqlalchemy.orm import joinedload
from fastapi import UploadFile
from enum import Enum
import os
from app.exceptions import ObjectNotFoundError,InvalidDataError
folder_path = os.path.join(os.path.abspath('.'), f"app/media/items")

class SortType(Enum):
    by_rating = "rating_desc"
    to_increase = "price_desc"
    to_decrease = "price_asc"
    by_date = "date_desc"
    by_preference = "by_preference"



def get_all_items(limit_num:int, page:int,sort_type:SortType,filters:ItemFilterSchema,user_id:int,currency_type:CurrencyType,session):
    items_query = session.query(Item).options(joinedload(Item.comments),
                                              joinedload(Item.images),
                                              joinedload(Item.categories)).filter(Item.is_active == True)
    #фильтрация
    if filters.min_price:
        items_query = items_query.filter(Item.price >= convert_currency(currency_type,CurrencyType.USD,filters.min_price))
    if filters.max_price:
        items_query = items_query.filter(Item.price <= convert_currency(currency_type,CurrencyType.USD,filters.max_price))
    if filters.category:

        def get_all_child_category_ids(category_id):
            category_ids = [category_id]
            child_categories = session.query(Category.id).filter(Category.parent_id == category_id).all()
            for child in child_categories:
                category_ids.extend(get_all_child_category_ids(child.id))
            return category_ids

        all_category_ids = get_all_child_category_ids(filters.category)
        items_query = items_query.filter(Item.category_id.in_(all_category_ids))

    #сортировка по базовым полям
    if sort_type == SortType.to_decrease:
        items_query = items_query.order_by(Item.price)
    elif sort_type == SortType.to_increase:
        items_query = items_query.order_by(Item.price.desc())
    elif sort_type == SortType.by_date:
        items_query = items_query.order_by(Item.created_at)


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
            res_images = [im for im in item.images if im.is_main == True][0].url
            if not res_images:
                res_images = None
        else:
            res_images = None
        res_data.append(ItemCatalogSchema(id=item.id, name=item.name, images=res_images,
                             price=convert_currency(CurrencyType.USD,currency_type,item.price), rating=rating))

    # соотировка по расчетным полям
    if sort_type == SortType.by_rating:
        res_data.sort(key=lambda x: x.rating if x.rating else False,reverse=True)
    elif sort_type == SortType.by_preference:
        if not user_id:
            raise ObjectNotFoundError("Нет пользователя")
        user = session.query(User).filter(User.id == user_id).first()
        user_tags_dict = {preference.tag_id: preference.score for preference in user.user_tag_preferences}
        def get_item_score(item_id):
            item_to_calculate = session.query(Item).filter(Item.is_active == True, Item.id == item_id).first()
            applied_item_tags = [tag.tag_id for tag in item_to_calculate.item_tags if
                                 tag.id in user_tags_dict.keys()]
            item_score = sum([score for tag_id, score in user_tags_dict.items() if tag_id in applied_item_tags])
            return item_score
        res_data.sort(key = lambda x:get_item_score(x.id))
    max_page = (len(res_data)//limit_num if len(res_data)/limit_num == len(res_data)//limit_num else len(res_data)//limit_num + 1)
    res_data = res_data[(page-1)*limit_num:(page-1)*limit_num+limit_num]

    return CatalogSchema(items=res_data,current_page=page,max_page=max_page)



def serv_get_item(item_id:int,user_id:int,currency_type:CurrencyType,session):
    item = session.query(Item).options(joinedload(Item.comments),
                                       joinedload(Item.images)).filter(Item.id ==item_id,
                                                                       Item.is_active == True).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    rating = None
    if item.comments:
        ratings = [com.rating for com in item.comments if com.rating is not None]
        if ratings:
            rating = round(sum(ratings) / len(ratings),1)

    attr_arr = [{f"{attr.attributes.name}": AttributeData(value=attr.value, unit=attr.unit)} for
                attr in item.attributes_value]
    if user_id:
        update_user_preference(user_id,item_id,session)

    item.views_count +=1
    return ItemSoloSchema(id = item.id,name = item.name,images = item.images, attributes=attr_arr,
                          price = convert_currency(CurrencyType.USD,currency_type,item.price),rating = rating,info= item.info,stock = item.stock)


async def create_item(add_item:ItemCreateSchema, media: list[UploadFile] | None ,session):
    if media:
        if len(media) != len(add_item.image_metadata):
            raise InvalidDataError("Кол-во metadata не совпадает с кол-вом image")
        if len([el for el in add_item.image_metadata if el == True]) != 1:
            raise InvalidDataError("Не выбрана/выбрано силшком много главных картинок")
        if len(media)>5:
            raise InvalidDataError("допускается не больше 5 фото на товар")

    item = Item(name = add_item.name,info = add_item.info,price = add_item.price,stock = add_item.stock,category_id = add_item.category_id)
    session.add(item)
    session.flush()
    db_images = []
    if media:
        for ind, file in enumerate(media):
            path = os.path.join(folder_path, f"{item.id}.{ind}.{file.filename.split('.')[1]}")
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_images.append(Image(url = path, is_main = add_item.image_metadata[ind],item_id = item.id))
    session.add_all(db_images)

    attributes = session.query(Attribute).filter(Attribute.category_id == add_item.category_id).all()
    if not all([attribute.id in add_item.attributes.keys() for attribute in attributes]) or len(attributes) != len(add_item.attributes):
        raise InvalidDataError("Недопустимые атрибуты")
    attr_to_add = [AttributeValue(attribute_id = attr_id,value = attr_data.value,
                                  unit = attr_data.unit,item_id = item.id) for attr_id,attr_data in add_item.attributes.items()]
    session.add_all(attr_to_add)

    all_tags = session.query(Tag).all()
    if not all([tag in [i.id for i in all_tags] for tag in add_item.tags]):
        raise InvalidDataError("Недопустимые тэги")

    tags_to_add = [ItemTag(tag_id = tag,item_id = item.id) for tag in add_item.tags]
    session.add_all(tags_to_add)
    session.flush()
    attr_arr = [{f"{attr.attributes.name}": AttributeData(value=attr.value,unit=attr.unit) } for
                attr in item.attributes_value]
    return ItemSoloSchema(id = item.id,name = item.name,images = item.images,attributes=attr_arr,
                          price = item.price,rating = None,info= item.info,stock = item.stock)


def serv_delete_item(item_id,session):
    item = session.query(Item).filter(Item.id == item_id,
                                      Item.is_active == True).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    item.is_active = False
    items_in_basket = item.basket_items
    if items_in_basket:
        for i in items_in_basket:
            session.delete(i)


async def serv_patch_item(item_id:int, new_data:ItemPatchSchema,media:list[UploadFile]|None,session):
    item = session.query(Item).filter(Item.id == item_id,
                                      Item.is_active == True).first()
    if not item:
        raise ObjectNotFoundError("Item not found")
    if new_data or media:
        item.updated_at = datetime.datetime.now()

    if new_data.category_id is not None and new_data.category_id != item.category_id:
        session.query(AttributeValue).filter_by(item_id=item.id).delete()
        item.category_id = new_data.category_id

    if media:
        if len(media) != len(new_data.image_metadata):
            raise InvalidDataError("Кол-во metadata не совпадает с кол-вом image")
        if len([el for el in new_data.image_metadata if el == True]) != 1:
            raise InvalidDataError("Не выбрана/выбрано силшком много главных картинок")
        if len(media) > 5:
            raise InvalidDataError("допускается не больше 5 фото на товар")

        [os.remove(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if
         os.path.isfile(os.path.join(folder_path, f)) and f"{item.id}." in f]

        db_images = []
        for ind, file in enumerate(media):
            path = os.path.join(folder_path, f"{item.id}.{ind}.{file.filename.split('.')[1]}")
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_images.append(Image(url=path, is_main=new_data.image_metadata[ind], item_id=item.id))

        session.query(Image).filter_by(item_id = item.id).delete()
        session.add_all(db_images)

    attributes = session.query(Attribute).filter(Attribute.category_id == item.category_id).all()
    if new_data.attributes:
        if not all([attribute.id in new_data.attributes.keys() for attribute in attributes]) or len(attributes) != len(new_data.attributes):
            raise InvalidDataError("Недопустимые атрибуты")
        attr_to_add = [AttributeValue(attribute_id=attr_id, value=attr_data.value,
                                      unit= attr_data.unit, item_id=item.id) for attr_id, attr_data in new_data.attributes.items()]
        session.query(AttributeValue).filter_by(item_id=item.id).delete()
        session.add_all(attr_to_add)
        new_data.attributes = None
    if new_data.tags:
        all_tags = session.query(Tag).all()
        if not all([tag in [i.id for i in all_tags] for tag in new_data.tags]):
            raise InvalidDataError("Недопустимые тэги")

        tags_to_add = [ItemTag(tag_id=tag, item_id=item.id) for tag in new_data.tags]
        session.query(ItemTag).filter_by(item_id=item.id).delete()
        session.add_all(tags_to_add)
        new_data.tags = None

    for key,value in new_data.model_dump(exclude_none=True).items():
        setattr(item,key,value)
    session.flush()

    rating = None
    if item.comments:
        ratings = [com.rating for com in item.comments if com.rating is not None]
        if ratings:
            rating = round(sum(ratings) / len(ratings), 1)


    attr_arr = [{f"{attr.attributes.name}": AttributeData(value=attr.value, unit=attr.unit)} for
                attr in item.attributes_value]

    return ItemSoloSchema(id=item.id, name=item.name, images=item.images, attributes=attr_arr,
                          price=item.price, rating=rating, info=item.info, stock=item.stock)


def serv_get_categories(session):
    categories = session.query(Category).all()

    category_dict = {cat.id: {'id': cat.id, 'name': cat.name, 'parent_id': cat.parent_id, 'children': []}
                     for cat in categories}

    root_categories = []
    for cat in categories:
        if cat.parent_id and cat.parent_id in category_dict:
            category_dict[cat.parent_id]['children'].append(category_dict[cat.id])
        else:
            root_categories.append(category_dict[cat.id])

    return root_categories
