from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "BG Remover API"
    admin_api_key: str = "bg_admin_test_12345"

    free_limit: int = 50
    basic_limit: int = 50
    pro_limit: int = 5_000
    ultra_limit: int = 25_000
    mega_limit: int = 100_000


settings = Settings()