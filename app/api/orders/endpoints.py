
from fastapi import APIRouter,status,Depends
from app.api.orders.services import serv_create_order,serv_get_all_orders
from app.core.dependencies import get_token,check_permissions
from app.api.orders.schemas import OrderSchema
from app.api.users.schemas import UserTokenDataSchema
from app.core.database import get_session
from sqlalchemy.orm.session import Session
from app.models.permission import ResourceEnum as Res, ActionEnum as Act
router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me",response_model=list[OrderSchema],
            dependencies=[Depends(check_permissions(Res.ORDERS,Act.READ))])
def get_my_order(user: UserTokenDataSchema = Depends(get_token),
                 session:Session = Depends(get_session)
                 ):
    response = serv_get_all_orders(user.id,session)
    return response

@router.post("/create",response_model=OrderSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.ORDERS,Act.CREATE))])
def create_order(user: UserTokenDataSchema = Depends(get_token),
                 session:Session = Depends(get_session)
                 ):
    response = serv_create_order(user.id,session)
    return response
