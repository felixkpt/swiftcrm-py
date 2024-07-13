# app/services/search_repo.py
from sqlalchemy import or_

def search_and_sort(query, Model, search_fields, query_params):
    # Apply search filters
    if query_params and query_params.search:
        search_filters = [
            getattr(Model, field).ilike(f"%{query_params.search}%")
            for field in search_fields
        ]
        query = query.filter(or_(*search_filters))

    # Apply sorting
    if query_params and query_params.order_by:
        if query_params.order_direction and query_params.order_direction.lower() == 'desc':
            query = query.order_by(getattr(Model, query_params.order_by).desc())
        else:
            query = query.order_by(getattr(Model, query_params.order_by))

    return query
