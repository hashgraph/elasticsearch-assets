__copyright__ = "Metrika"
__author__ = "Vasilis Adamopoulos, Chris Fergus"


import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Common env vars
    HEDERA_APP_PATH: str = os.getenv("HEDERA_APP_PATH")
    HEDERA_SCRIPTS_PATH: str = os.getenv("HEDERA_SCRIPTS_PATH")
    HEDERA_APP_CONFIG_PATH: str = os.getenv("HEDERA_APP_CONFIG_PATH")
    HEDERA_DEV_ENV: bool = os.getenv("HEDERA_DEV_ENV", "True")
    LOG_DIR: str = os.getenv("LOG_DIR")
    GOOGLE_APP_CREDENTIALS: str = os.getenv("GOOGLE_APP_CREDENTIALS")
    MIRROR_NODE_URL: str = os.getenv("MIRROR_NODE_URL")

    HEDERA_BUCKET_NAME: str = os.getenv("HEDERA_BUCKET_NAME")
    HEDERA_BUCKET_NODE: str = os.getenv("HEDERA_BUCKET_NODE")
    ALT_NODES: str = os.getenv("ALT_NODES")
    RECORDS_BUCKET_PREFIX: str = os.getenv("RECORDS_BUCKET_PREFIX")
    RECORDS_FILE_EXTENSION: str = os.getenv("RECORDS_FILE_EXTENSION")

    RECORDS_FILES_PATH: str = os.getenv("RECORDS_FILES_PATH")
    PARSED_RECORD_STREAM_FILES_DIR: str = os.getenv("PARSED_RECORD_STREAM_FILES_DIR")
    PARSED_RECORD_BALANCE_FILES_PATH: str = os.getenv("PARSED_RECORD_BALANCE_FILES_PATH")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    # Local info
    HEDERA_NETWORK: str = os.getenv("HEDERA_NETWORK")

    # Downloader sleep time between consecutive parses
    DOWNLOADER_LOOP_SLEEP: int = os.getenv("DOWNLOADER_LOOP_SLEEP", 5)
    # Orchestrator sleep time between consecutive parses
    ORCHESTRATOR_LOOP_SLEEP: int = os.getenv("ORCHESTRATOR_LOOP_SLEEP", 1)

    # Retention days used by mirror-node-cleaner for cleanup
    MIRROR_NODE_CLEANER_RETENTION_DAYS: int = os.getenv("MIRROR_NODE_CLEANER_RETENTION_DAYS", 7)


class Config:
    case_sensitive = True


settings = Settings()
