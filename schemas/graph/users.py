import strawberry
from db.connect import get_db, db
from typing import Any
from schemas.user import ReadUser
from schemas.profile import ProfileBase
from typing import Union, List


@strawberry.type
class RequestStatus:
    status:int = 200
    message:list[str]

@strawberry.experimental.pydantic.type(ProfileBase, all_fields=True)
class Profile:
    pass
    # first_name:strawberry.auto
    # last_name:strawberry.auto
    # phone_number:strawberry.auto
    # image:strawberry.auto



# @strawberry.type
# @strawberry.experimental.pydantic.type(model=ReadUser, all_fields=True)
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
    




