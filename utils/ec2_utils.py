import logging
import os

import boto3
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class EC2Utils:
    def __init__(self):
        self.__aws_region = os.getenv("AWS_REGION")
        if self.__aws_region is None or self.__aws_region == "":
            raise RuntimeError("aws region is not set")

        self._ec2_client = boto3.client("ec2", region_name=self.__aws_region)

    def get_instance_id_from_ip(self, ip_address: str):
        try:
            logger.info("Resolving instance id from ip=%s", ip_address)

            response = self._ec2_client.describe_instances(
                Filters=[
                    {'Name': 'private-ip-address', 'Values': [ip_address]}
                ]
            )

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance["InstanceId"]
                    logger.info("Resolved instance id=%s from ip=%s",instance_id, ip_address)
                    return instance_id

            logger.warning("No instance found for ip=%s",ip_address)
            raise HTTPException(status_code=404, detail=f"No instance found with IP: {ip_address}")
        except self._ec2_client.exceptions.ClientError as e:
            raise HTTPException(status_code=500, detail=f"AWS Error: {str(e)}")
