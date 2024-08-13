from pydantic import BaseModel

class Plot(BaseModel):
    file_id: int
    series_id: int
    style: str