from fastapi import APIRouter

router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me")
def get_my_order(user_id:int):
    pass

@router.post("/create")
def create_order():
    pass