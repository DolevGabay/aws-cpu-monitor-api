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

## Test

```bash
curl "http://localhost:8000/cpu-metrics?ip_address=172.31.88.161&start_time=2026-01-25T10:00:00&interval_seconds=300"
```