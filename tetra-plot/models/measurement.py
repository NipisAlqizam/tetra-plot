from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Measurement(BaseModel):
    id: Optional[int]
    series_id: int
    timestamp: datetime
    x: Optional[float]
    y: float
    comment: str
