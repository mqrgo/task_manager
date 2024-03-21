from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserData(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        checker = [
            len(value) >= 8,
            ' ' not in value,
            any([True if i.isupper() else False for i in value]),
            any([True if i.islower() else False for i in value]),
            any([True if i.isdigit() else False for i in value]),
            any([True if i in '!@#$%^&*()_+=-{}' else False for i in value])
        ]

        if all(checker):
            return value
        else:
            raise TypeError('password is not safe enough')


class TokenInfo(BaseModel):
    token: str
    token_type: str = 'Bearer'
