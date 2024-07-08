from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.validators import check_file_present
from app.core.user import current_user
from app.s3.s3 import s3_client
from app.schemas.s3 import FileData, S3File, S3Message

router = APIRouter()


@router.get(
    '/{file}',
    dependencies=(Depends(current_user),),
    response_model=Union[FileData, S3Message]
)
async def get_file(file: str):
    await check_file_present(file)
    try:
        data = await s3_client.get_file_data_base64(file)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    return {"data": data} if data else {"message": 'Error: File not found'}


@router.get(
    '/',
    dependencies=(Depends(current_user),),
    response_model=Union[S3File, S3Message]
)
async def list_file():
    try:
        file = await s3_client.list_files()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    return {"file": file}


@router.post(
    '/',
    response_model=S3Message,
    dependencies=(Depends(current_user),)
)
async def post_file(
    file: UploadFile = File(...),
):
    try:
        await s3_client.upload_to_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    return {"message": "File uploaded successfully"}


@router.delete(
    '/{file}',
    response_model=S3Message,
    dependencies=(Depends(current_user),)
)
async def delete_file(
    file: str,
):
    await check_file_present(file)
    try:
        await s3_client.delete_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )
    return {"message": "Ok"}
