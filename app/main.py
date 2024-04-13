import time
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.auth_sqladmin import authentication_backend
from app.bookings import router_bookings
from app.config.database import engine
from app.config.sentry import settings
from app.hotels import router_hotels, router_rooms
from app.images import router_images
from app.logger import logger
from app.pages import router_page
from app.users import router_auth

sentry_sdk.init(
    dsn=settings.DSN,
    enable_tracing=True,
    traces_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/sentry-debug")
async def trigger_error():
    return 1 / 0


@app.get("/memory_consumer")
def memory_consumer():
    _ = [i for i in range(10_000_000)]
    return 1


app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_page)
app.include_router(router_images)


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    lifespan=lifespan,
)

instrumentator = Instrumentator(
    should_group_status_codes=False, excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request execution time", extra={"process_time": process_time})
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089, reload=True)
