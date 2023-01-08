import math
import random
from fastapi import FastAPI

app = FastAPI(title='Mock API')

@app.get('/products/{id}/discount')
def get_product_discount(id: int):
    return { "discount": random.randint(0, 100) }