import asyncio
import base64
from contextlib import asynccontextmanager
from http import HTTPStatus

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

from app.core.config import settings


class S3Client:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.s3_access_key,
            "aws_secret_access_key": settings.s3_secret_key,
            "endpoint_url": settings.s3_endpoint_url,
            'verify': settings.s3_verify,  # При ошибке SSL в Windows -> False
        }
        self.bucket_name = settings.s3_bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ):
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    response = await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )

    async def upload_to_file(
            self,
            file: UploadFile,
    ):
        try:
            async with self.get_client() as client:
                contents = await file.read()
                response = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file.filename,
                    Body=contents,
                )
                print(f"File {file.filename} "
                      f"uploaded to {self.bucket_name}"
                      f"response {response}")
        except ClientError as e:
            print(f"Error uploading file: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )

    async def get_file_data_base64(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                data = await response["Body"].read()
                return base64.b64encode(data).decode('utf-8')
        except ClientError as e:
            print(f"Error downloading file: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )


    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=object_name
                )
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )

    async def list_files(self):
        try:
            async with self.get_client() as client:
                response = await client.list_objects_v2(
                    Bucket=self.bucket_name
                )
                return [item['Key'] for item in response["Contents"]]
        except ClientError as e:
            print(f"Error listing files: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )

    async def get_file_url(self, object_name: str):
        try:
            async with self.get_client() as client:

                url = await client.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": object_name,
                    },
                    ExpiresIn=0,
                )
                return url
        except ClientError as e:
            print(f"Error getting file URL: {e}")
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail=e,
            )


s3_client = S3Client()


async def main():


    # Проверка, что можем загрузить, скачать и удалить файл
    # await s3_client.upload_file("1.jpg")
    url = await s3_client.get_file_url('1.jpg')
    print(url)
    # await s3_client.get_file("1.jpg", "text_local_1.jpg")
    # await s3_client.delete_file("1.jpg")


if __name__ == "__main__":
    asyncio.run(main())
