from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./krushiai.db"
    cors_origins: str = "http://localhost:5173"
    weather_provider: str = "open_meteo"
    weather_api_key: str = ""
    llm_provider: str = "local"
    llm_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
