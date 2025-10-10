from fastapi import APIRouter, HTTPException,status, Depends
from app.services.api_crud.user import get_user,patch_user
from app.schemas.user import UserPatch,UserSchema,UserTokenDataSchema
from app.services.security import get_token

router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema)
def get_user_me(user:UserTokenDataSchema = Depends(get_token)):
    try:
        response = get_user(user.id)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/me",response_model=UserSchema)
def patch_user_me(user_data:UserPatch,user: UserTokenDataSchema = Depends(get_token)):
    try:
        response = patch_user(user.id,user_data)
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
