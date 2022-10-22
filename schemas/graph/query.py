import strawberry
from .users import UserQuery, UserCreateMutation
from .profile import ProfileQuery

@strawberry.type
class Query(UserQuery, ProfileQuery):
    pass

@strawberry.type
class Mutaions(UserCreateMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutaions)
