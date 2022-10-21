import strawberry

@strawberry.type
class Profile:
    first_name:str=""
    last_name:str=""
    phone_number:str=""
    image:str=""


@strawberry.type
class ProfileQuery:
    @strawberry.field
    def profile(self) -> Profile:
        return Profile(first_name="ali",last_name="Mahdavi",phone_number="09303444354",image="Null")
