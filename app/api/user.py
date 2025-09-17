from fastapi import APIRouter, HTTPException,status, Depends
from app.services.user import get_user,patch_user, user_by_token
from app.schemas.user import UserPatch, UserToken,UserSchema


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema)
def get_user_me(user: UserToken = Depends(user_by_token)):
    try:
        response = get_user(user.id)
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


@router.patch("/me",response_model=UserSchema)
def patch_user_me(user_data:UserPatch,user: UserToken = Depends(user_by_token)):
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
