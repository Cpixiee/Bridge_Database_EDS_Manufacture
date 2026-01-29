from typing import List

from fastapi import APIRouter, Depends, HTTPException
from mysql.connector import MySQLConnection, Error

from ..database import get_db
from ..schemas import User, APIResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("", response_model=APIResponse)
def list_users(db: MySQLConnection = Depends(get_db)) -> APIResponse:
    """
    Mengambil semua data dari tabel `users`.
    """
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()

        # Mapping hasil query ke list[User] jika field cocok
        users: List[User] = [User(**row) for row in rows]  # type: ignore[arg-type]

        return APIResponse(
            status="success",
            message="Users fetched successfully",
            data=users,
        )
    except Error as e:
        # Error dari MySQL
        raise HTTPException(status_code=500, detail=f"Database error: {e}") from e
    except Exception as e:  # noqa: BLE001
        # Error lain yang tidak terduga
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e


