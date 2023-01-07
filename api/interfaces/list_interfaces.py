from typing import Optional
from pydantic import BaseModel


class ListInterface(BaseModel):
    limit: int
    offset: Optional[int] = 0

class SearchableListInterface(ListInterface):
    q: Optional[str]