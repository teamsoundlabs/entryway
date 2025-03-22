# Quart import
from quart import Blueprint, abort, g, render_template, request
from quart_schema import validate_request, DataSource

# Database imports
from documents import Request
from model import SubmissionRequest, CaptchaCompleted

# Utility imports
import os
import logging
import datetime
from redis.asyncio import Redis
from cloudstile import AsyncTurnstile

# Initialise the blueprint
bp = Blueprint("verify", __name__)
logger = logging.getLogger(__name__)
turnstile = AsyncTurnstile(
    os.environ.get(
        "CLOUDFLARE_TURNSTILE_SECRET_KEY", "1x0000000000000000000000000000000AA"
    )
)


@bp.post("/verify/<id>/")
@validate_request(SubmissionRequest, source=DataSource.FORM)
async def verifyPost(id: str, data: SubmissionRequest):
    """Handle the verification post request."""

    response = await turnstile.validate(data.turnstile, request.remote_addr)
    if not response.success:
        return (
            await render_template(
                "/pages/error.jinja",
                code=409,
                message="Cloudflare failed authenticate you, please try again.",
            ),
            409,
        )

    document = await Request.find_one(Request.requestId == id)
    if document is None:
        return (
            await render_template(
                "/pages/error.jinja",
                code=404,
                message="The verification request has expired or has already been used. If you didn't complete the verification process, please request a new verification URL.",
            ),
            404,
        )

    elif document.expires_at < datetime.datetime.now(datetime.timezone.utc):

        return

    redis: Redis = g.redis
    await redis.publish(
        "encore_entryway_completions",
        CaptchaCompleted(
            user=document.user.id, server=document.server.id, entryId=id
        ).model_dump_json(),
    )

    await document.delete()

    return await render_template(
        "/pages/completed.jinja",
        user=document.user,
        server=document.server,
    )


@bp.get("/verify/<id>/")
async def verify(id: str):
    """Render the verification page if the token exists."""
    # Check if the token exists in the database
    request = await Request.find_one(Request.requestId == id)

    # If the token does not exist, return a 404
    if request is None:
        return (
            await render_template(
                "/pages/error.jinja",
                code=404,
                message="We were unable to find a verification request matching the entered URL. The request may have expired  already been completed by someone.",
            ),
            404,
        )

    # Render the verification page
    return (
        await render_template(
            "/pages/verify.jinja",
            user=request.user,
            server=request.server,
            id=id,
        ),
        200,
    )
