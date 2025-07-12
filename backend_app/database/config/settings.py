from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "The Global Payment Network"
    LOG_LEVEL: str = "INFO"
    
    # Security settings
    SECRET_KEY: str # Expects this from the environment (.env file)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    # Celery & Redis settings
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        # This tells pydantic to load the variables from a file named .env
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a single, importable settings instance for the rest of the application
settings = Settings()