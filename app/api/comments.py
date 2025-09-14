from fastapi import APIRouter

router = APIRouter(prefix="/comments",tags=["Comments"])

#юзер по токену

@router.get("/comments")
def get_comments(item_id:int, user:str):
    pass

@router.patch("/comments")
def patch_comments(item_id:int):
    pass

@router.delete("/comments")
def delete_comments(item_id:int):
    pass

@router.post("/comments")
def post_comments(item_id:int):
    pass







