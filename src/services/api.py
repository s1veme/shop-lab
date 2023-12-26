import http
import logging
import urllib.parse

import httpx

from services.base import SingletonService

logger = logging.getLogger(__name__)


class APIService(SingletonService):
    URL_ALL_PRODUCTS = '/api/v1/products'
    URL_ORDERS = '/api/v1/orders'
    URL_HEALTH = '/api/common/health'

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_products(self) -> list[dict]:
        url = self.build_url(self.URL_ALL_PRODUCTS)

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'failed to fetch products: {e}')
            return []

    def search_products(self, query: str) -> list[dict]:
        url = self.build_url(self.URL_ALL_PRODUCTS)
        url = f'{url}?search={query}'

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'failed to fetch products: {e}')
            return []

    def create_order(self, order: dict, access_token: str) -> dict:
        url = self.build_url(self.URL_ORDERS)

        try:
            with httpx.Client(follow_redirects=True, headers={'Authorization': f'Bearer {access_token}'}) as client:
                response = client.post(url, json=order)
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'Failed to fetch products. Error: {e}')
            return {}

    def health(self) -> bool:
        url = self.build_url(self.URL_HEALTH)

        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url)
            if response.status_code != http.HTTPStatus.OK:
                logger.error('the backend is not available')
                return False
            return True

    def build_url(self, url: str) -> str:
        return urllib.parse.urljoin(self.base_url, url)
