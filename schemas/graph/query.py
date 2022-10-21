import strawberry
from .users import UserQuery
from .profile import ProfileQuery

@strawberry.type
class Query(UserQuery, ProfileQuery):
    pass



schema = strawberry.Schema(query=Query)
