def build_paginated_response(
    query,
    limit: int,
    offset: int,
):
    total = query.count()
    items = query.offset(offset).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(items) < total
    }