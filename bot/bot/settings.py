from pydantic import AnyUrl, BaseSettings, SecretStr


class BotSettings(BaseSettings):
    model_api_url: AnyUrl

    telegram_token: SecretStr

    hugging_face_api_url: AnyUrl
    hugging_face_api_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
