import uvicorn
from fastapi import FastAPI

from config.env import get_env
from routers.user_routes import user_router
from services.db_services import connect_db

MONGO_URI = get_env("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not setted up.")
db_connection = connect_db(MONGO_URI)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "hello neo"}


app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(get_env("PORT") or 8000),
        reload=True,
    )
