# app/requests/middleware/auth_middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import base64

USERNAME = "your_username"
PASSWORD = "your_password"

class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        if auth is None or not auth.startswith("Basic "):
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="Login required"'},
            )

        auth_decoded = base64.b64decode(auth[6:]).decode("utf-8")
        username, password = auth_decoded.split(":", 1)

        if username != USERNAME or password != PASSWORD:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return await call_next(request)

def auth_middleware(app):
    app.add_middleware(BasicAuthMiddleware)
    return app
