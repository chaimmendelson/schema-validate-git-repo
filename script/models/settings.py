from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    folder: Path = Field(
        ...,
        description="Folder to validate"
    )

    json_schema: Path = Field(
        ...,
        description="Path to schema JSON"
    )

    model_config = SettingsConfigDict(
        cli_parse_args=True,
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
    )