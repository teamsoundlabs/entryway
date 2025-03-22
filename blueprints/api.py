# Quart import
from quart import Blueprint
from quart import request
from quart_schema import tag
from quart_schema import validate_request

# Database imports
from documents import Request

# Utility imports
from utils import protected
from model import CreationRequest
from string import ascii_letters, digits
from random import choice
from datetime import timedelta

# Initialise the blueprint
bp = Blueprint("api", __name__)


@bp.post("/api/create-request/")
@validate_request(CreationRequest)
@protected()
@tag(["api"])
async def create(data: CreationRequest):

    id = "".join(choice(ascii_letters + digits) for _ in range(32))

    document = await Request(
        user=data.user,
        server=data.server,
        requestId=id,
    ).save()

    return {
        "message": "Request created successfully.",
        "id": id,
        "timeout": document.created_at + timedelta(minutes=5),
    }, 201
