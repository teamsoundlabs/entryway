# Quart imports
from quart import Quart
from quart import redirect
from quart import render_template
from quart import current_app
from quart import g
from quart_schema import QuartSchema

# Database imports
import redis
from documents import _all_
from beanie import init_beanie
from redis.asyncio import Redis
from motor.motor_asyncio import AsyncIOMotorClient

# Utility imports
import os
import asyncio
import logging
import logfire
from dotenv import load_dotenv
from pymongo.errors import OperationFailure

# AioDNS fix
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialise components
load_dotenv()
app = Quart(__name__)
QuartSchema(app)
redisClient = Redis.from_url(os.environ.get("REDIS_URI", "redis://localhost:6379/0"))
mongodb = AsyncIOMotorClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"))
database = mongodb[os.environ.get("MONGODB_DATABASE", "entryway")]
logger = logging.getLogger(__name__)

# Initialise Logfire instrumentation
logfire.configure()
app.asgi_app = logfire.instrument_asgi(
    app.asgi_app,  # type: ignore
    False,
    True,
)
logfire.instrument_redis()

# Blueprint imports
from blueprints.verify import bp

app.register_blueprint(bp)

from blueprints.api import bp

app.register_blueprint(bp)


async def healthTask():
    """Automatically checks both the Redis and MongoDB connection and sets the status accordingly."""
    while True:
        services = {}
        try:
            await redisClient.ping()
            services["redis"] = True
        except redis.ConnectionError:
            services["redis"] = False

        try:
            await mongodb["admin"].command("ping")
            services["mongodb"] = True
        except Exception:
            services["mongodb"] = False

        current_app.config["health"] = services
        current_app.config["overall_health"] = all(
            current_app.config["health"].values()
        )

        await asyncio.sleep(30)


@app.before_request
async def beforeRequest():
    g.health = current_app.config["overall_health"]
    g.redis = redisClient
    g.mongodb = mongodb


@app.context_processor
async def contextProcessor():
    return {"health": g.health}


@app.before_serving
async def before_serving():
    await init_beanie(
        database=database,
        document_models=_all_,
        multiprocessing_mode=True,
    )

    while True:
        try:
            await database["verification_requests"].create_index(
                [("createdAt", 1)],  # Field to index
                expireAfterSeconds=100 * 18,  # Expiration time in seconds
                name="created_at",
            )
            break
        except OperationFailure as e:
            if (
                "An equivalent index already exists with the same name but different"
                in str(e)
            ):
                logger.warning("Dropped collection index to update to new value")
                await database["verification_requests"].drop_index("created_at")
            else:
                raise e

    app.add_background_task(healthTask)


@app.get("/health")
async def index():
    health = {}

    health["services"] = {}

    for k, v in current_app.config["health"].items():

        health["services"][k] = {"status": v}

    health["health"] = current_app.config["overall_health"]

    return health


if __name__ == "__main__":
    app.run("0.0.0.0", port=3000, debug=True)
