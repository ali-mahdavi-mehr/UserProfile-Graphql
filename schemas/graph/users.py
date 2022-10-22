import strawberry
from db.connect import get_db, db
from typing import Any
from schemas.user import ReadUser
from schemas.profile import ProfileBase
from typing import Union, List, Optional, Dict
from pydantic import EmailStr
from api.utills import hash_password
from fastapi import HTTPException


@strawberry.type
class RequestStatus:
    status:int = 200
    message:list[str]

@strawberry.experimental.pydantic.type(ProfileBase, all_fields=True)
class Profile:
    pass


@strawberry.experimental.pydantic.type(model=ReadUser)
class User():
    profile:strawberry.auto
    username:strawberry.auto
    email:strawberry.auto
    response_status:RequestStatus=RequestStatus(message=["hi"], status=400)



@strawberry.type
class Users:
    users: List[User]
    response_status:RequestStatus

@strawberry.input
class ProfileInput:
    first_name:str = ""
    last_name:str=""
    phone_number:str= ""
    image:str= ""

@strawberry.input
class UserInput:
    username:str
    email:str
    password:str






async def get_users()->Users:
    message = ["request received"]
    status = 200
    try:
        users = db.users.find({}, {"username": 1, "email":1, "_id": -1, "profile": 1})
        users = await users.to_list(10)
        u = []
        print("start")
        for user in users:
            if user.get("profile"):
                user["profile"] = Profile(**user["profile"])
            else:
                pass
                # user["profile"] = Profile(first_name="", last_name="", phone_number="", image="")
            del user["_id"]

            u.append(User(**user))
        response = RequestStatus(message=message, status=status)
        return Users(users=u, response_status=response)

    except Exception as e:
        print("fghgf")
        message += [error for error in e.args]
        status = 204
        response = RequestStatus(message=message, status=status)
        return Users(users=users, response_status=response)
    



async def get_user(username:str)->User:
    message = ["request received"]
    status = 200
    try:
        user = await db.users.find_one({"username":username}, {"username": 1, "email":1, "_id": -1, "profile": 1})
        if not user:
            print("user Not found")
            raise Exception("User Not Found")

        
        message.append("user Founded Successfully")
        if user.get("profile"):
            user["profile"] = Profile(**user["profile"])
        else:
            user["profile"] = Profile(first_name="", last_name="", phone_number="", image="")

        response = RequestStatus(message=message, status=status)
        del user["_id"]

        return User(**user, response_status=response)

    except Exception as e:
        print("fghgf")
        message += [error for error in e.args]
        status = 204
        response = RequestStatus(message=message, status=status)
        return User(response_status=response)
    # del user["_id"]
    # return User(**user)
    
    


@strawberry.type
class UserQuery:
    get_user:User=strawberry.field(resolver=get_user)
    get_users:Users=strawberry.field(resolver=get_users)

async def validated_data(data:dict) -> dict:
    data["password"] = hash_password(data["password"])
    data["username"] = data["username"].lower()
    data["email"] = data["email"].lower()
    username_found = await db["users"].find_one({"username":data["username"]})
    email_found = await db["users"].find_one({"email":data["email"]})

    if username_found:
        raise HTTPException(409, "Username Already taken by another user")

    if email_found:
        raise HTTPException(409, "Email Already taken by another user")

    return data

@strawberry.type
class UserCreateMutation:
    @strawberry.mutation
    async def create_user(self, input:UserInput, profile:ProfileInput=None)->User:
        data = input.__dict__
        if profile:
            data["profile"] = profile.__dict__
            profile = Profile(**data["profile"])
        data = await validated_data(data)
        if data:
            new_user = await db.users.insert_one(data)
        user = User(username=input.username, email=input.email, profile=profile)

        return user



