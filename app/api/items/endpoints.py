from typing import Optional
from fastapi import APIRouter, status, Depends,Form,File, UploadFile
import json

from app.api.items.services import serv_get_item, get_all_items,SortType
from app.api.items.schemas import ItemFilterSchema,get_filters,CatalogSchema
from app.api.items.services import create_item,serv_delete_item, serv_patch_item
from app.api.items.schemas import ItemCreateSchema,ItemPatchSchema,ItemSoloSchema

from app.core.dependencies import TokenDep,check_permissions,SessionDep

from app.models.user import CurrencyType
from app.core.enums import ResourceEnum as Res, ActionEnum as Act



router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all",response_model=CatalogSchema,
            dependencies=[Depends(check_permissions(Res.ITEMS,Act.READ))])
def get_item_all(user:TokenDep,
                 session:SessionDep,
                 filters:ItemFilterSchema = Depends(get_filters),# replace into dependence
                 limit:int = 10,
                 page:int = 1,
                 sort_type:SortType = SortType.by_rating
                 ):
    response = get_all_items(limit,page,sort_type,filters,user.id,CurrencyType[user.currency],session)
    return response



@router.get("/{item_id}",response_model=ItemSoloSchema,
            dependencies=[Depends(check_permissions(Res.ITEMS,Act.READ))])
def get_item(item_id:int,
             user:TokenDep,
             session:SessionDep
             ):
    response = serv_get_item(item_id,user.id if user else None,CurrencyType(user.currency),session)
    return response


@router.post("/create",response_model=ItemSoloSchema,
             status_code=status.HTTP_201_CREATED,
             tags=["Admin"],
             dependencies=[Depends(check_permissions(Res.ITEMS, Act.CREATE))])
def post_item(session:SessionDep,
              name: str = Form(...),
              price: float = Form(...),
              info: str|None = Form(None),
              images: list[UploadFile] | None = File(None),
              image_metadata: str|None= Form(None),
              stock: int = Form(0),
              attributes: str = Form(...),
              tags: str = Form(...),
              category_id:int = Form(...)
              ):
        new_item = ItemCreateSchema(name = name,price = price,info = info,
                                    stock = stock,attributes = json.loads(attributes),
                                    image_metadata = json.loads(image_metadata) if image_metadata else None ,
                                    tags =json.loads(tags) ,category_id = category_id)
        response = create_item(new_item,images,session)
        return response



@router.patch("/{item_id}",response_model=ItemSoloSchema,
              tags=["Admin"],
              dependencies=[Depends(check_permissions(Res.ITEMS, Act.UPDATE))])
def patch_item( item_id:int|None,
                session:SessionDep,
                name: str = Form(None),
                price: Optional[float]= Form(None,),
                info: str|None = Form(None),
                images: list[UploadFile] | None = File(None),
                image_metadata: str | None = Form(None),
                stock: int|None = Form(None),
                attributes: str|None = Form(None),
                tags: str | None = Form(None),
                is_active:Optional[bool]= Form(None),
                category_id:int |None = Form(None)
                ):

        new_data = ItemPatchSchema(name = name,price = price,info = info,is_active = is_active,
                                    stock = stock,attributes = json.loads(attributes) if attributes else None,
                                    image_metadata = json.loads(image_metadata) if image_metadata else None,
                                    tags = json.loads(tags) if tags else None,category_id = category_id)
        response = serv_patch_item(item_id,new_data,images,session)
        return response



@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,
               tags=["Admin"],
               dependencies=[Depends(check_permissions(Res.ITEMS, Act.DELETE))])
def delete_item(item_id,session:SessionDep):
    serv_delete_item(item_id,session)
    return {"msg:":"Item deleted"}





