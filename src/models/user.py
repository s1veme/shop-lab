from dataclasses import dataclass

from models.base import Singleton


@dataclass
class CreateUser:
    username: str
    password: str


@dataclass
class User:
    username: str
    id: int | None = None


@dataclass(frozen=True)
class ActiveUser(metaclass=Singleton):
    username: str
    access_token: str
