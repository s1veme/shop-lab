from pathlib import Path

from models.user import User

WORK_DIR = Path(__file__).resolve().parent.parent

WIDTH = 1366
HEIGHT = 768

BASE_URL = 'http://127.0.0.1:8000'

USER: User | None = None
