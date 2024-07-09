# app/requests/validations/main_validator.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

class Validator:

    @staticmethod
    def validate_required_fields(model_request, required_fields):
        for field in required_fields:
            if getattr(model_request, field) is None or getattr(model_request, field) == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} is required."
                )

class UniqueChecker:

    @staticmethod
    def check_unique_fields(db: Session, model, model_request, unique_fields, model_id=None):
        for field in unique_fields:
            existing_record = db.query(model).filter(getattr(model, field) == getattr(model_request, field))
            if model_id:
                existing_record = existing_record.filter(model.id != model_id)
            if existing_record.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A record with this {field} already exists."
                )
