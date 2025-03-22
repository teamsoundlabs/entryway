from datetime import datetime, timezone, timedelta
from typing import Literal
from beanie import Document
from pydantic import BaseModel, Field, validator


class User(BaseModel):

    username: str

    display_name: str

    id: str


class Server(BaseModel):

    id: str

    name: str


def datetime_factory():
    return datetime.now(timezone.utc)


def expiry_factory():
    return datetime.now(timezone.utc) + timedelta(minutes=15)


class Request(Document):
    requestId: str

    user: User

    server: Server

    created_at: datetime = Field(default_factory=datetime_factory)

    expires_at: datetime = Field(default_factory=expiry_factory)

    state: Literal["uncompleted", "completed"] = "uncompleted"

    class Settings:

        name = "verification_requests"
