from pydantic import BaseModel


class S3Message(BaseModel):
    message: str


class S3File(BaseModel):
    file: list[str]


class FileData(BaseModel):
    data: str
