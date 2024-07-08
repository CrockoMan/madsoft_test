from fastapi import APIRouter

from app.api.endpoints import (
    s3_router, meme_router, user_router
)

main_router = APIRouter()
main_router.include_router(
    meme_router,
    prefix='/memes',
    tags=['Meme']
)
main_router.include_router(
    s3_router,
    prefix='/s3',
    tags=['S3']
)

main_router.include_router(user_router)
