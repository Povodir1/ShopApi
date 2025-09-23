
from fastapi import APIRouter,HTTPException,status
from app.services.order import serv_create_order,serv_get_all_orders
from app.schemas.order import OrderSchema
router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me",response_model=list[OrderSchema])
def get_my_order(user_id:int):
    response = serv_get_all_orders(user_id)
    return response

@router.post("/create",response_model=OrderSchema,status_code=status.HTTP_201_CREATED)
def create_order(user_id:int):
    try:
        response = serv_create_order(user_id)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )