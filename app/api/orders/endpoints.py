from fastapi import APIRouter,status,Depends

from app.api.orders.services import serv_create_order,serv_get_all_orders
from app.api.orders.schemas import OrderSchema

from app.core.dependencies import TokenDep,check_permissions,SessionDep

from app.core.enums import ResourceEnum as Res, ActionEnum as Act



router = APIRouter(prefix="/order",tags=["Order"])


@router.get("/me",response_model=list[OrderSchema],
            dependencies=[Depends(check_permissions(Res.ORDERS,Act.READ))])
def get_my_order(user:TokenDep,
                 session:SessionDep
                 ):
    response = serv_get_all_orders(user.id,session)
    return response

@router.post("/create",response_model=OrderSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.ORDERS,Act.CREATE))])
def create_order(user:TokenDep,
                 session:SessionDep
                 ):
    response = serv_create_order(user.id,session)
    return response
