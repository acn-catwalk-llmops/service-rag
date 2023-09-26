from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union


# Following is taken from:
# https://github.com/ChristopherGS/ultimate-fastapi-tutorial/tree/main/part-08-structure-and-versioning
# Left here for future reference if needed
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./env/.env", env_file_encoding="utf-8", case_sensitive=True
    )

    CHROMADB_HOST: str
    CHROMADB_PORT: int
    CHROMADB_USER: str
    CHROMADB_PASSWORD: str
    S3_BUCKET_DOCUMENTS: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
