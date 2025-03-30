from fastapi import FastAPI

from src.api.endpoints.user import router
from src.api.endpoints.auth import router as auth
from src.api.endpoints.admin import router as admin_router
from src.api.endpoints.auth_yandex import router as auth_yandex
from src.api.endpoints.audio import router as audio


def create_app() -> FastAPI:

    app = FastAPI()


    app.include_router(router, prefix="/api/v1")
    app.include_router(auth, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api")
    app.include_router(auth_yandex, prefix="/api")
    app.include_router(audio, prefix="/api")
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
