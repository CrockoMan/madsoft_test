from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_file_present, check_meme, check_meme_exists
)
from app.core.db import get_async_session
from app.crud.meme import meme_crud
from app.s3.s3 import s3_client
from app.schemas.meme import MemeBase, MemeGetDB
from app.utils import meme_with_path

router = APIRouter()


@router.get(
    '/{meme_id}',
    response_model=Optional[MemeBase],
)
async def get_meme(
        meme_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    meme = await check_meme_exists(meme_id, session)
    return meme_with_path(meme)


@router.get(
    '/',
    response_model=list[MemeGetDB],
)
async def get_all_memes(
        page: int = Query(1, gt=0),
        limit: int = Query(10, le=100),
        session: AsyncSession = Depends(get_async_session),
):
    meme = await meme_crud.get_multi_paginated(
        session,
        offset=(page - 1) * limit,
        limit=limit
    )
    return [meme_with_path(item, True) for item in meme]


@router.post(
    '/',
    response_model=Optional[MemeGetDB],
)
async def create_memes(
    file: UploadFile = File(...), text: str = "",
    session: AsyncSession = Depends(get_async_session),
):
    await check_meme(text, session)
    await check_file_present(file.filename)
    try:
        meme = await meme_crud.create(
            {
                'text': text,
                'file': file.filename
            },
            session,
            commit=False
        )
        await s3_client.upload_to_file(file)
        await session.commit()
        await session.refresh(meme)
        return meme
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.put(
    '/{meme_id}',
    response_model=Optional[MemeGetDB],
)
async def update_memes(
    meme_id: int,
    file: Optional[UploadFile] = File(...), text: Optional[str] = "",
    session: AsyncSession = Depends(get_async_session),
):
    meme = await meme_crud.get(meme_id, session)
    update_date = dict()
    if text:
        await check_meme(text, session)
        update_date['text'] = text
    if file:
        update_date['file'] = file
        await check_file_present(file.filename)
    try:
        meme = await meme_crud.update(update_date, session, commit=False)
        if file is not None:
            await s3_client.delete_file(file)
            await s3_client.upload_to_file(file)
        await session.commit()
        await session.refresh(meme)
        return meme
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    '/{meme_id}',
    response_model=MemeGetDB,
    response_model_exclude_none=True,
)
async def delete_memes(
    meeme_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    meme = await check_meme_exists(meeme_id, session)
    try:
        await s3_client.delete_file(meme.file)
        meme = await meme_crud.remove(meme, session)
        return meme
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
