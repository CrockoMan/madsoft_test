from sqlalchemy import Column, String, Text

from app.constants import TEXT_LIMIT
from app.core.db import Base

FILE_NAME_MAX_LEN = 50


class Meme(Base):
    text = Column(Text, nullable=False)
    file = Column(String(FILE_NAME_MAX_LEN), unique=True, nullable=False)

    def __repr__(self):
        return (
            f'"{self.text[:TEXT_LIMIT]}" {self.file}'
        )
