# app/main.py
from fastapi import FastAPI
from app.requests.middleware.cors import cors_middleware
from app.requests.middleware.auth import auth_middleware
from app.auto_routes_handler import auto_register_routes
from app.websocket.websocket_route_handlers import websocket_routes
import subprocess
import logging
from app.database.seeders.seed_data import seed_user
from contextlib import asynccontextmanager

# Initialize the FastAPI app
app = FastAPI()

# Initialize the database
# Base.metadata.create_all(bind=engine)

# Include CORS middleware
cors_middleware(app)

# Include authentication middleware
# auth_middleware(app)

# Add root endpoint

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCRM-PY!"}


# Automatically generate and register routes
auto_register_routes(app)

@app.get("/list-routes")
def list_routes():
    routes = []
    for route in app.routes:
        route_info = {
            "path": route.path,
            "methods": route.methods,
            "name": route.name,
            "handler": route.endpoint.__module__ + '.' + route.endpoint.__name__
        }
        routes.append(route_info)
    return routes

# Include WebSocket routes
app.include_router(websocket_routes)

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run Alembic migrations
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logging.info("Alembic migrations applied.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running Alembic migrations: {e}")

    # Seed the database
    seed_user()

    yield  # This is where the application is up and running

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    list_of_routes = list_routes()
    for route in list_of_routes:
        print(route)
