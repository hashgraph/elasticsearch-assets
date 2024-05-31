import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Bucket(BaseModel):
    name: Optional[str]


class Blob(BaseModel):
    name: Optional[str]
    bucket: Optional[Bucket]
    size: Optional[str]
    updated: Optional[datetime.datetime]
    content_type: Optional[str]
