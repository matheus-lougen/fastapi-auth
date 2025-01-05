from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Dataclass for acessing the enviroment variables

    Attributes:
        model_config (SettingsConfigDict): Settings for loading the enviroment variables from `.env` file.
        DATABASE_URL (str): Database connection URL.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: str
