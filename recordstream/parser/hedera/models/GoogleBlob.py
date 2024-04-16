from typing import Optional

from pydantic import BaseModel


class Bucket(BaseModel):
    name: Optional[str]


class GoogleBlob(BaseModel):
    name: Optional[str]
    bucket: Bucket = Bucket(name="0")
    size: Optional[str]
    update: Optional[str]
    content_type: Optional[str]
