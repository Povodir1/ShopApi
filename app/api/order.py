from fastapi import APIRouter
from app.services.order import serv_create_order,serv_get_all_orders

router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me")
def get_my_order(user_id:int):
    return serv_get_all_orders(user_id)

@router.post("/create")
def create_order(user_id:int):
    return serv_create_order(user_id)