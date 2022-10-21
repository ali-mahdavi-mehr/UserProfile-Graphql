from pydantic import BaseModel, Field, EmailStr
from schemas.profile import ProfileBase
from typing import Optional

class BaseUser(BaseModel):
    _id:Field(str, alias="_id")
    username:str=""
    email:str=""
    class Config:
        allowed_population_by_field_name=True
        arbitrary_types_allowed=True




class createUser(BaseUser):
    password:str=Field(...)
    username:str=Field(...)
    email:EmailStr=Field(...)
    class Config:
        schema_extra = {
            "example":{
                "username": "Ali",
                "email":"test@example.com",
                "password": "password"
            }
        }

class ReadUser(BaseUser):
    profile:Optional[ProfileBase]
    
