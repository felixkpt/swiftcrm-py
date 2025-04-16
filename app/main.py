from fastapi import FastAPI
from app.requests.middleware.cors import cors_middleware
from app.requests.middleware.auth import auth_middleware
from app.auto_routes_handler import auto_register_routes
from app.websocket.websocket_route_handlers import websocket_routes
import subprocess
import logging
from app.database.seeders.seed_data import seed_user
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    await asyncio.sleep(10)

    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logging.info("Alembic migrations applied.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running Alembic migrations: {e}")

    seed_user()

    yield  # app is running

# Passing the lifespan to the FastAPI app
app = FastAPI(lifespan=lifespan)

cors_middleware(app)
# auth_middleware(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to SwiftCRM-PY!"}

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

app.include_router(websocket_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
