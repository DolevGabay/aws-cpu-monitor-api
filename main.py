import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from objects.datapoint import Datapoint
from services.cpu_metrics_service import CpuMetricsService

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"]
)

logger = logging.getLogger(__name__)
cpu_metrics_service = CpuMetricsService()

@app.get("/")
def root():
    return {"message": "AWS CPU Monitor API", "docs": "/docs"}

@app.get("/cpu-metrics", response_model=list[Datapoint])
def get_cpu_metrics(ip_address: str, start_time: datetime, interval_seconds: int, end_time: Optional[datetime] = None):
    try:
        logger.info("Getting cpu metrics for ip=%s start_time=%s interval_seconds=%s end_time=%s", ip_address, start_time, interval_seconds, end_time)

        datapoints = cpu_metrics_service.get_cpu_metrics(
            ip_address=ip_address,
            start_time=start_time,
            interval_seconds=interval_seconds,
            end_time = end_time
        )

        logger.info("Successfully returned %s datapoints", len(datapoints))
        return datapoints
    except HTTPException as e:
        logger.warning(f"Client error: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error for ip={ip_address}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
