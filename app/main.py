from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.products import router as products_router
from app.routes.orders import router as orders_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade e-commerce backend API",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All routers registered here
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "running",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }