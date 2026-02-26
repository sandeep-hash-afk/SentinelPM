# SentinelPM — Predictive Maintenance Intelligence

SentinelPM is a production-ready predictive maintenance intelligence service, prioritizing reliability and explainability over black-box models .

## 🌐 Live Demo

SentinelPM is deployed and publicly accessible:

**Base URL:**  
https://sentinelpm.onrender.com/

**Interactive API Docs:**  
https://sentinelpm.onrender.com/docs

**Health Check:**  
https://sentinelpm.onrender.com/health

# Problem
Unplanned equipment failures cause:
-	Costly downtime
-	Safety risks
-	Reactive maintenance

Although sensors generate large amounts of data, most systems:
-	Alert too late
-	Produce noisy signals
- Provide no clear action

# Solution
SentinelPM:
-	Analyzes sensor readings (temperature, vibration, voltage)
-	Detects early warning signs of failure
-	Communicates clear, actionable decisions
-	Operates safely under strict validation and observability


# System Capabilities
-	Sensor health evaluation API
-	Human-centered decision output
-	Strict input validation
-	Payload size protection
-	Safe failure handling
-	Structured logging & latency tracking
-	Dockerized deployment
-	CI-validated builds

# API
## Endpoint
POST /predict

## Input
{
  "temperature": 92,
  "vibration": 78,
  "voltage": 230
}

## Output
{
  "status": "Fault detected",
  "reason": "Abnormal sensor readings observed",
  "confidence_level": "High",
  "recommended_action": "Immediate inspection recommended"
}

## Run locally
uvicorn app.main:app --reload

## Docker
docker build -t sentinelpm .
docker run -p 8000:8000 sentinelpm


# Security & Reliability
-	Rejects unexpected input fields
-	Enforces payload size limits
-	Logs metadata only (no raw data)
-	Safe fallback behavior on failures
-	No hallucination-prone outputs

# Scope (v1)
Included:
-	Sensor health assessment
-	Decision & action recommendation
-	Production readiness

Excluded (intentionally):
-	Dashboards
-	User authentication
-	Streaming ingestion
-	Automated retraining