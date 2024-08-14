from pydantic import BaseModel

class Plot(BaseModel):
    file_id: str
    series_id: int
    style: str