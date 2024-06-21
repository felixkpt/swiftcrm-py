# app/requests/middleware/cors_middleware.py

from fastapi.middleware.cors import CORSMiddleware

def cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this as needed to specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
