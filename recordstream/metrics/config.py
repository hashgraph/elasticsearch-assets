__copyright__ = "Metrika"
__author__ = "Vasilis Adamopoulos, Chris Fergus, Ngan Le"


import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Common env vars
    HEDERA_APP_CONFIG_PATH: str = os.getenv("HEDERA_METRIC_CONFIG_PATH")
    HEDERA_DEV_ENV: bool = os.getenv("HEDERA_DEV_ENV", "True")
    LOG_DIR: str = os.getenv("LOG_DIR")
    PARSER_OUTPUT_DIR: str = os.getenv("PARSER_OUTPUT_DIR")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    # Local info
    HEDERA_NETWORK: str = os.getenv("HEDERA_NETWORK")


class Config:
    case_sensitive = True


settings = Settings()
