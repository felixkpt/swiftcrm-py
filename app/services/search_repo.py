# app/services/search_repo.py
from sqlalchemy import or_
from fastapi import Request

def apply_search_and_sort(query, Model, search_fields, query_params):
    # Apply search filters
    if query_params and query_params.get('search'):
        search_filters = [
            getattr(Model, field).ilike(f"%{query_params['search']}%")
            for field in search_fields
        ]
        query = query.filter(or_(*search_filters))

    # Apply sorting
    if query_params and query_params.get('order_by'):
        if query_params.get('order_direction') and query_params['order_direction'].lower() == 'desc':
            query = query.order_by(getattr(Model, query_params['order_by']).desc())
        else:
            query = query.order_by(getattr(Model, query_params['order_by']))

    return query

def get_query_params(request: Request, default_search_fields=['name', 'description']):
    params = request.query_params
    query_params = {
        'search': params.get("search", ""),
        'search_fields': default_search_fields,
        'order_by': params.get("order_by", ""),
        'order_direction': params.get("order_direction", ""),
        'page': int(params.get("page", 1)),
        'limit': int(params.get("limit", 10)),
    }
    return query_params
