from dataclasses import dataclass


@dataclass
class Order:
    full_name: str
    address: str
    email: str
    product_id: int

    user_id: int = 1
    id: int | None = None
