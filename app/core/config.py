from pydantic import BaseSettings, Field


class S3Settings(BaseSettings):
    s3_access_key: str = Field('s3_access_key', env='S3_ACCESS_KEY')
    s3_secret_key: str = Field('s3_secret_key', env='S3_SECRET_KEY')
    s3_endpoint_url: str = Field('s3_endpoint_url', env='S3_ENDPOINT_URL')
    s3_bucket_name: str = Field('s3_bucket_name', env='S3_BUCKET_NAME')
    s3_verify: bool = False
    s3_bucket_public_path: str = Field(
        's3_bucket_public_path',
        env='S3_BUCKET_PUBLIC_PATH'
    )

    class Config:
        env_file = '.env'


class AppSettings(BaseSettings):
    app_title: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config(BaseSettings):
        env_file = '.env'


class Settings(AppSettings, S3Settings):
    pass


settings = Settings()
