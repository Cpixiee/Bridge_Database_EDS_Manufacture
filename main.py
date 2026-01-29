from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import users, qa


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Konfigurasi CORS agar Flutter (web/mobile) bisa akses backend ini
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # production sebaiknya di-restrict
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Daftarkan router
    app.include_router(users.router)
    app.include_router(qa.router)

    @app.get("/api/v1/health")
    def health_check():
        return {"status": "ok", "message": "Cyber Backend API is running"}

    return app


app = create_app()


