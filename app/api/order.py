
from fastapi import APIRouter,HTTPException,status,Depends
from app.services.order import serv_create_order,serv_get_all_orders
from app.services.security import get_token
from app.schemas.order import OrderSchema
from app.services.user import UserTokenDataSchema
router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me",response_model=list[OrderSchema])
def get_my_order(user: UserTokenDataSchema = Depends(get_token)):
    response = serv_get_all_orders(user.id)
    return response

@router.post("/create",response_model=OrderSchema,status_code=status.HTTP_201_CREATED)
def create_order(user: UserTokenDataSchema = Depends(get_token)):
    try:
        response = serv_create_order(user.id)
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