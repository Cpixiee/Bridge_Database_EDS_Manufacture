import re
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from mysql.connector import MySQLConnection, Error

from ..database import get_db
from ..schemas import APIResponse
from ..config import get_settings

router = APIRouter(prefix="/api/v1/qa", tags=["QA Database"])


TABLE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def _validate_table_name(table_name: str) -> str:
    """
    Validasi sederhana untuk mencegah SQL injection via nama tabel.
    Hanya mengizinkan huruf, angka, dan underscore.
    """
    if not TABLE_NAME_PATTERN.fullmatch(table_name):
        raise HTTPException(status_code=400, detail="Invalid table name")
    return table_name


@router.get("/tables", response_model=APIResponse)
def list_tables(db: MySQLConnection = Depends(get_db)) -> APIResponse:
    """
    Mengambil daftar semua tabel di database `qa`.
    """
    settings = get_settings()
    try:
        cursor = db.cursor()
        # Gunakan query yang lebih eksplisit dengan nama database
        cursor.execute(f"SHOW TABLES FROM `{settings.db_name}`")
        rows = cursor.fetchall()
        cursor.close()

        tables: List[str] = [row[0] for row in rows]

        return APIResponse(
            status="success",
            message="Tables fetched successfully",
            data=tables,
        )
    except Error as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}. Check DB connection to {settings.db_host}:{settings.db_port}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        ) from e


@router.get("/{table_name}", response_model=APIResponse)
def get_table_data(
    table_name: str,
    limit: int = Query(100, ge=1, le=1000),
    db: MySQLConnection = Depends(get_db),
) -> APIResponse:
    """
    Mengambil data dari tabel tertentu di database `qa`.

    Contoh:
    - GET /api/v1/qa/barcode_qa
    - GET /api/v1/qa/chopper?limit=50
    """
    table_name = _validate_table_name(table_name)

    try:
        cursor = db.cursor(dictionary=True)
        query = f"SELECT * FROM `{table_name}` LIMIT %s"
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        cursor.close()

        return APIResponse(
            status="success",
            message=f"Data fetched from table '{table_name}'",
            data=rows,
        )
    except Error as e:
        # Misalnya tabel tidak ada, dsb.
        raise HTTPException(status_code=500, detail=f"Database error: {e}") from e


