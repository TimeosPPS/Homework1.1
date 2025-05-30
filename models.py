from pydantic import BaseModel, Field

from typing import Optional, List, Dict, Annotated, Union
from pydantic.networks import EmailStr
from pydantic import field_validator
import re
import string

class BooksModel(BaseModel):
    id: Annotated[int,Field(0, description="Id of the book", examples=[0, 1, 2], ge=0, le = 71)]
    userId: Annotated[int, Field(description="Id of the user", examples=[1, 2, 3], ge=1, le=10)]
    title: Annotated[str, Field(description="Title of the book", examples=["qui est esse", "eum et est occaecati"], min_length=3, max_length=50)]
    body: Annotated[str, Field(description="Body of the book", examples=["quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto", "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"], min_length=3, max_length=200)]

class BooksModelResponse(BooksModel):
    pass


class UserModel(BaseModel):
    firstName: Annotated[str, Field(..., min_length=2, description="First name of the user")]
    lastName: Annotated[str, Field(..., min_length=2, description="Last name of the user")]
    email: Annotated[Optional[EmailStr], Field(None, description="Email of the user")]
    password: Annotated[str, Field(..., min_length=8, description="Ім'я: мінімум 2 символи, лише літери. Прізвище: мінімум 2 символи, лише літери. Електронна пошта: має бути валідною електронною адресою. Пароль: мінімум 8 символів, повинен містити хоча б одну велику літеру, одну маленьку літеру, одну цифру та один спеціальний символ. Номер телефону: має відповідати патерну мобільного телефону.")]
    phone_number: Annotated[Optional[str], Field(None, description="Phone number of the user", examples=["+38(063)123-45-67"])]

    @field_validator("firstName")
    def first_name_validator(cls, value: str):
        if value.isalpha():
            return value
        raise ValueError("First name must contain only letters")
    
    @field_validator("lastName")
    def last_name_validator(cls, value: str):
        if value.isalpha():
            return value
        raise ValueError("Last name must contain only letters")
    
    @field_validator("phone_number")
    def phone_number_validator(cls, value: Optional[str]):
        if value and not re.search(r"\+380\(0\d{2}\)\d{3}-\d{2}-\d{2}", value):
            raise ValueError("Phone number must match the pattern +380(0XX)XXX-XX-XX")
        return value
    
    @field_validator("password")
    def password_validator(cls, value: str):
        is_upper = False
        is_lower = False
        is_digit = False
        is_punctuation = False

        for char in value:
            if not is_upper and char.isupper():
                is_upper = True
            if not is_lower and char.islower():
                is_lower = True
            if not is_digit and char.isdigit():
                is_digit = True
            if not is_punctuation and char in string.punctuation:
                is_punctuation = True
        if all([is_upper, is_lower, is_digit, is_punctuation]):
            return value