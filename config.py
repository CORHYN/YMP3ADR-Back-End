from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    allowed_origin: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()