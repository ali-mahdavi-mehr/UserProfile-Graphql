from pydantic import BaseModel, Field, EmailStr, StrBytes
# from schemas.user import BaseUser
from typing import Optional

class ProfileBase(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    phone_number:Optional[str]
    image:Optional[bytes]
    class Config:
        allowed_population_by_field_name=True
        arbitrary_types_allowed=True
        



class UpdateProfile(ProfileBase):
    class Config:
        schema_extra = {
        "example":{
            "first_name": "Ali",
            "last_name": "Mahdavi",
            "phone_number": "Ali",
            "image":""
        }
    }

