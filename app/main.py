import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.bookings import router_bookings
from app.users import router_auth
from app.hotels import router_hotels
from app.hotels import router_rooms
from app.pages import router_page
from app.images import router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_page)
app.include_router(router_images)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089, reload=True)
