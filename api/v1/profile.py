from fastapi import APIRouter, Depends, HTTPException
from db.connect import get_db
from schemas import profile, user
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/profile")


@router.post("/", response_model=user.ReadUser)
async def add_profile(data:profile.UpdateProfile, username:str , db=Depends(get_db)):
    updated_user = await db["users"].find_one({"username": username})
    if not updated_user:
        raise HTTPException(404, "User Not Found!")
    data = jsonable_encoder(data)
    result = await db["users"].update_one({"username": updated_user["username"]}, {"$set": {"profile":data}})
    updated_user = await db["users"].find_one({"username": username})
    return updated_user
