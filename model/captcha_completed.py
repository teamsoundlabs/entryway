from pydantic import BaseModel


class CaptchaCompleted(BaseModel):

    user: str

    server: str

    entryId: str
