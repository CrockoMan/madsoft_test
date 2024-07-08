from fastapi import UploadFile
from pydantic import BaseModel, Field


class MemeGetDB(BaseModel):
    id: int = Field(..., title='id')
    text: str = Field(..., title='Текст')
    file: str = Field(..., title='Файл')

    class Config:
        orm_mode = True


class MemeBase(BaseModel):
    text: str = Field(..., title='Текст')
    file: str = Field(..., title='Файл')


class MemeOneDB(MemeBase):
    pass

    class Config:
        orm_mode = True


class MemeCreate(BaseModel):
    text: str = Field(..., title='Текст')
    file: UploadFile
