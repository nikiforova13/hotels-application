import datetime
from datetime import date

import uvicorn
from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles
from app.bookings import bookings_router
from app.users import router_auth
from app.hotels import hotels_router
from app.hotels import rooms_router
from app.pages import router_page
from app.images import router_images
app = FastAPI()

app.mount(path='/static', app=StaticFiles(directory='app/static'), name="static")
app.include_router(router_auth)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(router_page)
app.include_router(router_images)





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089, reload=True)
