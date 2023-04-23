from pydantic import BaseSettings

class Settings(BaseSettings):
  DB_USER:str
  DB_HOST:str
  DB_NAME:str
  DB_PASSWORD:str
  JWT_ALGORITHM:str
  API_PASSWORD:str
  
  class Config:
    env_file=".env"

settings = Settings()