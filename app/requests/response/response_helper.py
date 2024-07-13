from fastapi import HTTPException, status

class ResponseHelper:

    @staticmethod
    def format_error(error_type: str, loc: list, msg: str, input_value: any, url: str):
        return {
            "type": error_type,
            "loc": loc,
            "msg": msg,
            "input": input_value,
            "url": url
        }

    @staticmethod
    def raise_http_exception(error_type: str, loc: list, msg: str, input_value: any, url: str, status_code=status.HTTP_400_BAD_REQUEST):
        raise HTTPException(
            status_code=status_code,
            detail=ResponseHelper.format_error(error_type, loc, msg, input_value, url)
        )

    @staticmethod
    def handle_integrity_error(e: Exception):
        # Assuming 'e.orig' contains information about the unique constraint failure
        return ResponseHelper.raise_http_exception(
            error_type="unique_constraint",
            loc=["body"],
            msg="Failed to create record. Possibly due to unique constraint.",
            input_value=str(e.orig),
            url="https://errors.pydantic.dev/2.8/v/unique_constraint"
        )

    @staticmethod
    def handle_not_found_error(model_id: int):
        return ResponseHelper.raise_http_exception(
            error_type="not_found",
            loc=["path", "model_id"],
            msg="Record not found.",
            input_value=model_id,
            url="https://errors.pydantic.dev/2.8/v/not_found",
            status_code=status.HTTP_404_NOT_FOUND
        )
