from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from utils.cloudwatch_utils import CloudwatchUtils
from utils.ec2_utils import EC2Utils


class CpuMetricsService:
    def __init__(self):
        self.__ec2_utils = EC2Utils()
        self.__cloudwatch_utils = CloudwatchUtils()

    def get_cpu_metrics(self, ip_address: str, start_time: datetime, interval_seconds: int, end_time: Optional[datetime] = None):
        if interval_seconds < 1:
            raise HTTPException(status_code=400, detail="interval_seconds must be at least 1")

        if end_time is None:
            end_time = datetime.utcnow()

        if start_time >= end_time:
            raise HTTPException(status_code=400, detail="start_time must be before end_time")

        instance_id = self.__ec2_utils.get_instance_id_from_ip(ip_address)

        datapoints = self.__cloudwatch_utils.get_cpu_metrics(
            instance_id=instance_id,
            start_time=start_time,
            interval_seconds=interval_seconds,
            end_time=end_time
        )

        return datapoints
