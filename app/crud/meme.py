from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meme import Meme


class CRUDMeme(CRUDBase):

    async def get_meme_by_text(
        self,
        text: str,
        session: AsyncSession,
    ) -> Optional[Meme]:
        meme = await session.execute(
            select(Meme).filter(
                Meme.text == text,
            )
        )
        return meme.scalars().first()

    async def get_multi_paginated(
            self,
            session: AsyncSession,
            offset: int,
            limit: int
    ):
        db_objs = await session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            commit=True
    ):
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)

        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


meme_crud = CRUDMeme(Meme)
