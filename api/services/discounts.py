from fastapi import Depends
from requests import request
from api.settings import Settings, get_settings


class DiscountsService:

    def __init__(self, settings: Settings = Depends(get_settings)):
        self.discounts_url = settings.discounts_api_base

    def get_discount(self, product_id: int):
        url = f"{self.discounts_url}/products/{product_id}/discount"
        discounts_response = request('GET', url)
        if discounts_response.status_code >= 400:
            return { "discount": 0 }
        return discounts_response.json()['discount']

def get_discounts_service(settings: Settings = Depends(get_settings)):
    return DiscountsService(settings=settings)