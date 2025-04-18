# app/services/search_repo.py
from sqlalchemy import or_
from fastapi import Request


def apply_common_filters(query, Model, search_fields, query_params):
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
            query = query.order_by(
                getattr(Model, query_params['order_by']).desc())
        else:
            query = query.order_by(getattr(Model, query_params['order_by']))
    else:
        # Default ordering by id in descending order
        query = query.order_by(Model.id.desc())

    # Apply status filter
    if 'status_id' in query_params:
        status_id = query_params['status_id']
        if status_id != 0:
            query = query.filter(Model.status_id == status_id)
    else:
        query = query.filter(Model.status_id == 1)

    return query


def get_query_params(request: Request, default_search_fields=['name', 'description']):
    # Extract dynamic attributes from request.state._state
    state_params = getattr(request.state, '_state', {})

    params = request.query_params
    query_params = {
        'search': params.get("search", ""),
        'search_fields': default_search_fields,
        'order_by': params.get("order_by", "id"),
        'order_direction': params.get("order_direction", "desc"),
        'page': int(params.get("page", 1)),
        'per_page': int(params.get("per_page", 10)),
    }
    return {**request.query_params, **query_params, **state_params}


def set_metadata(query, query_params):
    total_records = query.count()
    metadata = {
        "per_page": query_params['per_page'],
        "page": int(query_params['page'] or 1),
        "order_by": query_params.get('order_by', None),
        "order_direction": query_params.get('order_direction', None),
        "total_records": total_records,
    }
    return metadata
