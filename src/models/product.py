from dataclasses import dataclass


@dataclass
class Product:
    id: int
    title: str
    description: str
    price: int
    image: str
