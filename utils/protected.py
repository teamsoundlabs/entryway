from functools import wraps
from typing import Callable, Any
from quart import request
from quart import abort
from httpx import AsyncClient
import logging
import os


def comp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False


logger = logging.getLogger(__name__)

unkeyBearer = os.environ.get("UNKEY_BEARER", None)
unkeyApiId = os.environ.get("UNKEY_API_ID", None)
if not unkeyApiId or not unkeyBearer:
    logger.error(
        "UNKEY_BEARER or UNKEY_API_ID are unset, any protected requests will be dropped until you set them."
    )


def protected(permissions: list[str] = []) -> Callable:
    """ "
    Args:
        permissions (list[str]): A list of permissions required to access the route.
    Raises:
        401: If the Authorization header is missing or the token is invalid.
        403: If the provided API key is missing required permissions.
        503: If the bearer token is not available.
    """

    def decorator(func: Callable) -> Callable:

        # Fail-safe for missing Unkey authentication
        if not unkeyApiId or not unkeyBearer:

            @wraps(func)
            async def fail():
                abort(503)

            return fail

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with AsyncClient(
                base_url="https://api.unkey.dev",
                headers={
                    "Authorization": f"Bearer {unkeyBearer}",
                    "Content-Type": "application/json",
                },
            ) as session:

                header = request.headers.get("Authorization")
                if header is None:
                    abort(401)

                resp = await session.post(
                    url="/v1/keys.verifyKey",
                    json={
                        "apiId": unkeyApiId,
                        "key": header,
                    },
                )
                response: dict = resp.json()

                if resp.status_code != 200:
                    logger.error(
                        "Recived %s from Unkey",
                        response.get("error", {}).get("code", "NILL"),
                    )
                    abort(503)
                    return

                comp(permissions, response.get("permissions", []))

                return await func(*args, **kwargs)

        return wrapper

    return decorator
