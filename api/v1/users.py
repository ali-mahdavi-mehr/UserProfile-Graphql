from fastapi import APIRouter, Depends, HTTPException
from db.connect import get_db
from schemas import user, profile
from fastapi.encoders import jsonable_encoder
from typing import List
from api.utills import hash_password

router = APIRouter(prefix="/users")


@router.post("/", response_model=user.ReadUser)
async def new_user(data:user.createUser, db=Depends(get_db)):
    data = jsonable_encoder(data)
    data["username"] = data["username"].lower()
    data["email"] = data["email"].lower()
    username_found = await db["users"].find_one({"username":data["username"]})
    email_found = await db["users"].find_one({"email":data["email"]})

    if username_found:
        raise HTTPException(409, "Username Already taken by another user")

    if email_found:
        raise HTTPException(409, "Email Already taken by another user")

    data["password"] = hash_password(data['password'])
    result = await db["users"].insert_one(data)
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    return created_user


@router.get("/", response_model=List[user.ReadUser])
async def get_users(db=Depends(get_db)):
    users = db.users.find()
    users = await users.to_list(10)
    return users


@router.get("/{username}", response_model=user.ReadUser)
async def get_user(username:str, db=Depends(get_db)):
    selected_user = await db["users"].find_one({"username":username.lower()})
    if not selected_user:
        raise HTTPException(404, "User Not Found")

    return selected_user


@router.delete("/{username}")
async def delete_user(username:str, db=Depends(get_db)):
    selected_user = await db.users.find_one({"username":{"$eq":username}})
    if not selected_user:
        raise HTTPException(404, "User not found!")

    await db.users.delete_one({"username": {"$eq": username}})
    return {"status": 204}


