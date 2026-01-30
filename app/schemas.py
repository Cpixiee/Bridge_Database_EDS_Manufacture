from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class User(BaseModel):
    """
    Schema untuk 1 row pada tabel `users`.
    Sesuaikan field di sini dengan struktur kolom sebenarnya di database.
    """

    id: int
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None


class APIResponse(BaseModel):
    """
    Bentuk response standar API.
    """

    status: str
    message: str
    data: Optional[Any] = None  # Changed from Any | None for Python 3.9 compatibility


