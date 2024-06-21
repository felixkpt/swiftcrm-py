from .model_table_generator import generate_model_table
from .crud_generator import generate_crud
from .routes_generator import generate_routes
from .schema_generator import generate_schema
import asyncio

async def async_generate_model_table(model_name, fields):
    await asyncio.sleep(1)  # Simulating an asynchronous operation
    generate_model_table(model_name, fields)

async def async_generate_crud(model_name, fields):
    await asyncio.sleep(1)  # Simulating an asynchronous operation
    generate_crud(model_name, fields)

async def async_generate_schema(model_name, fields):
    await asyncio.sleep(1)  # Simulating an asynchronous operation
    generate_schema(model_name, fields)

async def async_generate_routes(model_name):
    await asyncio.sleep(2)  # Simulating an asynchronous operation
    generate_routes(model_name)

def auto_model_handler(data):
    model_name = data.modelName
    fields = data.fields

    tasks = [
        async_generate_model_table(model_name, fields),
        async_generate_crud(model_name, fields),
        async_generate_schema(model_name, fields),
        async_generate_routes(model_name)
    ]

    asyncio.gather(*tasks)
