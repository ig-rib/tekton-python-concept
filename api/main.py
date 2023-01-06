from fastapi import FastAPI
from routers.healthchecks import healthchecks_router

app = FastAPI()

app.include_router(healthchecks_router, "/healthcheck")