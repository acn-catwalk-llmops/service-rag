from pydantic_settings import BaseSettings, SettingsConfigDict


# Following is taken from:
# https://github.com/ChristopherGS/ultimate-fastapi-tutorial/tree/main/part-08-structure-and-versioning
# Left here for future reference if needed
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./env/.env", env_file_encoding="utf-8", case_sensitive=True
    )

    VECTORSTORE_HOST: str
    VECTORSTORE_PORT: int
    VECTORSTORE_USER: str | None = None
    VECTORSTORE_PASSWORD: str | None = None
    VECTORSTORE_PASSWORD: str | None = None

    AWS_REGION: str = "eu-central-1"
    AWS_ACCES_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_DOCUMENTS: str

    OPENAI_APIKEY: str
    OPENAI_API_KEY: str

    TRANSFORMERS_OFFLINE: int = 1


settings = Settings()
