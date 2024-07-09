# app/main.py
from fastapi import FastAPI
from app.requests.middleware.cors import cors_middleware
from app.requests.middleware.auth import auth_middleware
from app.auto_routes_handler import auto_register_routes
from fastapi import FastAPI
from app.repositories.database import setup_database

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

@app.get("/setup-database")
async def set_database():
    setup_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    list_of_routes = list_routes()
    for route in list_of_routes:
        print(route)
