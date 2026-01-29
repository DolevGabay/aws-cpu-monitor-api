# AWS Instance CPU Monitor

## Setup

```bash
pip install -r requirements.txt 
```

## Environment Variables

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

## Run

```bash
python main.py
```

## API

### GET /cpu-metrics

Fetches CPU utilization metrics for a specific EC2 instance over a given time range using AWS CloudWatch.

**Query Parameters**

- `ip_address` (string) - Private IP address of the EC2 instance
- `start_time` (datetime) - Start of the time range (UTC)
- `end_time` (datetime) - End of the time range (UTC). Defaults to current UTC time
- `interval_seconds` (integer) - CloudWatch sampling interval (period), in seconds (minimum: 60)

**Example Request**

```bash
curl "http://localhost:8000/cpu-metrics?ip_address=172.31.88.161&start_time=2026-01-25T10:00:00Z&interval_seconds=300"
```

**Example Response**

```json
[
  {
    "timestamp": "2026-01-25T10:00:00Z",
    "average": 12.43,
    "unit": "Percent"
  },
  {
    "timestamp": "2026-01-25T10:05:00Z",
    "average": 15.01,
    "unit": "Percent"
  }
]
```
