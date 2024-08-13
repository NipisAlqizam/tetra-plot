from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Measurement(BaseModel):
    id: int
    series_id: int
    timestamp: datetime
    x: Optional[int]
    y: int
    comment: Optional[str]