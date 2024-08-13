from pydantic import BaseModel

class Series(BaseModel):
    id: int
    user_id: int
    title: str
    x_name: str = "Время"
    y_name: str
