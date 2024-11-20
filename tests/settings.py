from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bsky_username: str
    bsky_password: str
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
