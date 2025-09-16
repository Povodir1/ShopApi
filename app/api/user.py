from fastapi import APIRouter, HTTPException,status, Depends
from app.services.user import get_user,patch_user, user_by_token
from app.schemas.user import UserPatch, UserToken,UserSchema


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema)
def get_user_me(user: UserToken = Depends(user_by_token)):
    response = get_user(user.id)
    return response


@router.patch("/me",response_model=UserSchema)
def patch_user_me(user_data:UserPatch,user: UserToken = Depends(user_by_token)):
    response = patch_user(user.id,user_data)
    return response
