from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_import
from app.logger import logger
from app.pages.router import router as router_pages
from app.pages.auth_router import router as router_auth
from app.pages.booking_router import router as router_booking
from app.pages.hotel_detail_router import router as router_hotel_detail
from app.pages.profile_router import router as router_profile
from app.prometheus.router import router as router_prometheus
from app.users.router import router as router_users


app = FastAPI(
    title="Бронирование Отелей",
    root_path="/api",
)


app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_pages)
app.include_router(router_auth)
app.include_router(router_booking)
app.include_router(router_hotel_detail)
app.include_router(router_profile)
app.include_router(router_images)
app.include_router(router_prometheus)
app.include_router(router_import)


# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    # redis = aioredis.from_url(
    #     f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    #     encoding="utf8",
    #     decode_responses=True,
    # )
    # FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[
        ".*admin.*",
        "/metrics"
    ]
)

instrumentator.instrument(app).expose(app)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/pages")
