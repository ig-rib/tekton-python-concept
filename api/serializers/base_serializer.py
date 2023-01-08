class BaseSerializer:
    
    def serialize(self, model):
        raise NotImplementedError()
    
    def serialize_paginated_list(self, items, page: int, limit :int, total_count: int):
        return {
            "page": page,
            "limit": limit,
            "totalCount": total_count,
            "items": [self.serialize(item) for item in items]
        }
