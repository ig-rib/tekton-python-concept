from fastapi import FastAPI
from routers.healthchecks import healthchecks_router

app = FastAPI(title='Products API', openapi_url='../openapi.yaml')

app.include_router(healthchecks_router, "/healthcheck")