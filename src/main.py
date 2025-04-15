from contextlib import asynccontextmanager
from typing import AsyncIterator, List

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.integrations.logger import logger

from .api.v1.docs.router import docs_router
from .integrations.metrics.metrics import metrics
from .integrations.metrics.middleware import prometheus_metrics
from .on_startup.logger import setup_logger


def setup_middleware(app: FastAPI) -> None:
    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(prometheus_metrics)


def setup_routers(app: FastAPI) -> None:
    routers: List[APIRouter] = [
        docs_router,
    ]
    app.add_route("/metrics", metrics)
    for router in routers:
        app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("START APP")
    setup_logger()
    yield
    logger.info("END APP")


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/swagger", lifespan=lifespan, default_response_class=ORJSONResponse)
    setup_middleware(app)
    setup_routers(app)
    return app
