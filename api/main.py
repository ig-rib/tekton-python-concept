import logging
import time

logging.info('Starting server')

from fastapi import FastAPI, Request
from api.routers.healthchecks import healthchecks_router
from api.routers.products import products_router


app = FastAPI(title='Products API')

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time)*1000)
    logging.info(f'{request.method} {request.url} returned {response.status_code} - Time Ellapsed: {process_time}ms')
    return response

    
app.include_router(healthchecks_router, prefix="/healthcheck")
app.include_router(products_router, prefix="/products")

from api.database.redis import redis_db
