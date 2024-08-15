from typing import Optional
from pydantic import BaseModel


class Series(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    x_name: str = "Время"
    y_name: str
