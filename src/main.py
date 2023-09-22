"""Main function"""
import sys
import uuid

import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.app_config import settings


def get_application():
    """Creating The App Instance"""
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
logger = loguru.logger
logger.remove()
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "{extra[ip]} {extra[user]} - <level>{message}</level>"
)
logger.configure(extra={"ip": "", "user": ""})  # Default values
logger.add(sys.stderr, format=logger_format)


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):
        logger.info("Request started")

        try:
            return await call_next(request)

        except Exception as ex:
            logger.error(f"Request failed: {ex}")
            return JSONResponse(content={"success": False}, status_code=500)

        finally:
            logger.info("Request ended")


# ADD Routes
