from typing import List
from fastapi import HTTPException

def validate_auto_page_builder_request(fields: List[dict], action_labels: List[dict], headers: List[dict]):
    if not fields:
        raise HTTPException(status_code=400, detail="Fields must not be empty.")
    if not action_labels:
        raise HTTPException(status_code=400, detail="Action labels must not be empty.")
    if not headers:
        raise HTTPException(status_code=400, detail="Headers must not be empty.")
