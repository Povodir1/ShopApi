
from fastapi import APIRouter,HTTPException,status,Depends
from app.services.api_crud.order import serv_create_order,serv_get_all_orders
from app.services.security import get_token
from app.schemas.order import OrderSchema
from app.schemas.user import UserTokenDataSchema
from app.database import get_session
from sqlalchemy.orm.session import Session
router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me",response_model=list[OrderSchema])
def get_my_order(user: UserTokenDataSchema = Depends(get_token),session:Session = Depends(get_session)):
    response = serv_get_all_orders(user.id,session)
    return response

@router.post("/create",response_model=OrderSchema,status_code=status.HTTP_201_CREATED)
def create_order(user: UserTokenDataSchema = Depends(get_token),session:Session = Depends(get_session)):
    response = serv_create_order(user.id,session)
    return response
