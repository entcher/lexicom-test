from .validators import validate_phone_number
from pydantic import BaseModel, field_validator


class Data(BaseModel):
    phone: str | int
    address: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, number: str | int):
        if not validate_phone_number(number):
            raise ValueError('Wrong number format')        
        return number


class DataAddressOut(BaseModel):
    address: str
