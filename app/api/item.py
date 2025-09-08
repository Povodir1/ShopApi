from fastapi import APIRouter

router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all")
def get_item_all():
    pass


@router.get("/{item_id}")
def get_item_by_id(item_id):
    pass


@router.post("/create")
def create_item():
    pass


@router.patch("/{item_id}")
def patch_item_me(item_id):
    pass


@router.delete("/{item_id}")
def delete_item(item_id):
    pass