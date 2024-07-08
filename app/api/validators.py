from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    FILE_NOT_FOUND, MEME_EMPTY, MEME_EXISTS, MEME_NOT_FOUND
)
from app.crud.meme import meme_crud
from app.s3.s3 import s3_client


async def check_meme(
    text: str,
    session: AsyncSession,
) -> None:
    if text == '':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MEME_EMPTY,
        )
    meme = await meme_crud.get_meme_by_text(text, session)
    if meme is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=MEME_EXISTS,
        )


async def check_meme_exists(
    meme_id: int,
    session: AsyncSession,
):
    meme = await meme_crud.get(meme_id, session)
    if meme is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=MEME_NOT_FOUND
        )
    return meme


async def check_file_present(file: str) -> None:
    files = await s3_client.list_files()
    if file not in files:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=FILE_NOT_FOUND,
        )
