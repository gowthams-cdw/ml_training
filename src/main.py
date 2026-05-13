from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from config.env import get_env
from routers.user_routes import user_router
from routers.word_routes import word_router
from services.db_services import connect_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    MONGO_URI = get_env("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not setted up.")
    _db_connection = connect_db(MONGO_URI)

    yield

    print("Shutdown.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "hello neo"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, _exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "success": False,
            "message": "Validation failed",
        },
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    _request: Request,
    exc: StarletteHTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )


@app.exception_handler(Exception)
async def internal_server_error_handler(_request: Request, _exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "status_code": 500,
            "message": "Internal server error",
            "data": None,
        },
    )


app.include_router(user_router)
app.include_router(word_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(get_env("PORT") or 8000),
        reload=True,
    )
