from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, field_validator

class CpuMetricsQuery(BaseModel):
    ip_address: str
    start_time: datetime
    interval_seconds: int
    end_time: Optional[datetime] = None

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def enforce_utc(cls, value: datetime):
        if value is None:
            return value

        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone (UTC)")

        return value.astimezone(timezone.utc)
