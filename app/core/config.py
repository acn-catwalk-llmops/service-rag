from pydantic_settings import BaseSettings
from pathlib import Path


# Following is taken from:
# https://github.com/ChristopherGS/ultimate-fastapi-tutorial/tree/main/part-08-structure-and-versioning
# Left here for future reference if needed
class Settings(BaseSettings):
    VECTORSTORE_HOST: str
    VECTORSTORE_PORT: int
    VECTORSTORE_USER: str | None = None
    VECTORSTORE_PASSWORD: str | None = None
    VECTORSTORE_PASSWORD: str | None = None

    AWS_REGION: str = "eu-central-1"
    AWS_ACCES_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_DOCUMENTS: str

    OPENAI_API_KEY: str


PATH_TO_ENVFILE = "./env/.env"
envfile_exists = Path(PATH_TO_ENVFILE).is_file()
settings = Settings(
    _env_file=PATH_TO_ENVFILE if envfile_exists else None,
    _env_file_encoding="utf8" if envfile_exists else None,
    _case_sensitive=True,
)
