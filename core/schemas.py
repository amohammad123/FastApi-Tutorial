from typing import Optional

from pydantic import BaseModel, field_validator

class BasePersonSchema(BaseModel):
    name:str

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError('name must be between 1 and 32 characters long')
        if not value.isalpha():
            raise ValueError('name must contain only letters')
        return value

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonUpdateSchema(BasePersonSchema):
    pass

class PersonResponseSchema(BasePersonSchema):
    id: int

