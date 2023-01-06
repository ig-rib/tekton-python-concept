from fastapi import FastAPI
from api.routers.healthchecks import healthchecks_router
from api.routers.products import products_router

app = FastAPI(title='Products API')

app.include_router(healthchecks_router, prefix="/healthcheck")
app.include_router(products_router, prefix="/products")
