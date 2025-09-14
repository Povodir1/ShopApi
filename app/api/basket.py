from fastapi import APIRouter

router = APIRouter(prefix="/basket",tags=["basket"])


@router.get("/basket")
def get_basket():
    pass

@router.post("/basket")
def add_to_basket():
    pass

@router.delete("/basket")
def delete_from_basket():
    pass

@router.patch("/basket")
def patch_in_basket():
    pass
