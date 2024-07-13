# app/requests/validations/main_validator.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class Validator:

    @staticmethod
    def validate_required_fields(model_request, required_fields):
        errors = []
        for field in required_fields:
            if getattr(model_request, field) is None or getattr(model_request, field) == "":
                errors.append({
                    "type": "missing_field",
                    "loc": ["body", field],
                    "msg": f"{field} is required.",
                    "input": getattr(model_request, field),
                    "url": "https://errors.pydantic.dev/2.8/v/missing_field"
                })

        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors
            )


class UniqueChecker:

    @staticmethod
    def check_unique_fields(db: Session, model, model_request, unique_fields, model_id=None):
        errors = []
        for field in unique_fields:
            existing_record = db.query(model).filter(
                getattr(model, field) == getattr(model_request, field))
            if model_id:
                existing_record = existing_record.filter(model.id != model_id)
            if existing_record.first():
                errors.append({
                    "type": "unique_constraint",
                    "loc": ["body", field],
                    "msg": f"A record with this {field} already exists.",
                    "input": getattr(model_request, field),
                    "url": "https://errors.pydantic.dev/2.8/v/unique_constraint"
                })

        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors
            )
