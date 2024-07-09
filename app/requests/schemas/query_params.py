# app/requests/schemas/query_params.py
from pydantic import BaseModel

class QueryParams(BaseModel):
    page: int = 1
    limit: int = 10
    search: str = ""
    search_fields: list = []
    order_by: str = ""
    order_direction: str = ""