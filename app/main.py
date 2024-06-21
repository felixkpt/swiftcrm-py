from fastapi import FastAPI
from app.database.connection import engine
from app.models.base import Base
from app.routes import auto_page_builder
from app.requests.middleware import cors_middleware, auth_middleware

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database
# Base.metadata.create_all(bind=engine)

# Include CORS middleware
# app.middleware("http")(cors_middleware)

# Include authentication middleware
# app.middleware("http")(auth_middleware)

# Include routes
app.include_router(auto_page_builder.router,
                   prefix="/auto-page-builder", tags=["AutoPageBuilder"])

# Add root endpoint


@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCRM-PY!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
