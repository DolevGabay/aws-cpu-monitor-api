from datetime import datetime

from pydantic import BaseModel


class Datapoint(BaseModel):
    timestamp: datetime
    average: float
    unit: str
