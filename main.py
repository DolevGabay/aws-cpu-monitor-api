import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from objects.cpu_metrics_query import CpuMetricsQuery
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
    return {"message": "AWS CPU Monitor API"}

@app.get("/cpu-metrics", response_model=list[Datapoint])
def get_cpu_metrics(query: CpuMetricsQuery = Depends()):
    try:
        logger.info("Getting cpu metrics query=%s", query.model_dump())

        datapoints = cpu_metrics_service.get_cpu_metrics(
            ip_address=query.ip_address,
            start_time=query.start_time,
            interval_seconds=query.interval_seconds,
            end_time=query.end_time
        )

        logger.info("Successfully returned %s datapoints", len(datapoints))
        return datapoints
    except HTTPException as e:
        logger.warning(f"Client error: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error for ip={query.ip_address}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
