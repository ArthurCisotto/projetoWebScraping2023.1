import logging
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app import healthcheck, ocr

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"])
    application.include_router(healthcheck.router)
    application.include_router(ocr.router)

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
