from pydantic import BaseModel, Field
from documents.request import User, Server


class CreationRequest(BaseModel):

    user: User

    server: Server


class SubmissionRequest(BaseModel):

    turnstile: str = Field(alias="cf-turnstile-response")
