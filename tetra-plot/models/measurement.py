from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Measurement(BaseModel):
    id: Optional[int] = None
    series_id: int
    timestamp: datetime
    x: Optional[float] = None
    y: float
    comment: str
