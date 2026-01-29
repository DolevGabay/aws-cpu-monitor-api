import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from objects.datapoint import Datapoint

logger = logging.getLogger(__name__)


class CloudwatchUtils:
    def __init__(self):
        self.__aws_region = os.getenv("AWS_REGION")
        if not self.__aws_region:
            raise RuntimeError("aws region is not set")

        self._cloudwatch_client = boto3.client("cloudwatch", region_name=self.__aws_region)

    def get_cpu_metrics(self, instance_id: str, start_time: datetime, interval_seconds: int, end_time: datetime):
        try:
            logger.info("Getting cpu metrics for instance_id=%s start_time=%s interval_seconds=%s end_time=%s",instance_id, start_time, interval_seconds, end_time)

            response = self._cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {'Name': 'InstanceId', 'Value': instance_id}
                ],
                StartTime=start_time, # assumes UTC
                EndTime=end_time, # assumes UTC
                Period=interval_seconds,
                Statistics=['Average']
            )

            raw_datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp']) # CloudWatch returns datapoints in arbitrary order

            datapoints = [
                Datapoint(
                    timestamp=datapoint["Timestamp"],
                    average=round(datapoint['Average'], 2),
                    unit=datapoint['Unit']
                )
                for datapoint in raw_datapoints
            ]

            logger.info("Successfully got %s cpu datapoints for instance_id=%s", len(datapoints), instance_id)
            return datapoints
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "InvalidParameterCombination":
                raise HTTPException(status_code=400, detail="The selected time range and interval would return too many data points - max allowed is 1440")
            raise
