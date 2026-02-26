from fastapi import FastAPI, Request, HTTPException
from app.models import SensorInput
from app.services import predict_health
import logging
import time
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.decision_layer import explain_decision
from collections import defaultdict
import time
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

RATE_LIMIT = 60  # requests
WINDOW = 60      # seconds
requests_by_ip = defaultdict(list)


app = FastAPI(title="Sensor Health AI")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("sensor-health-ai")

@app.middleware("http")
async def limit_payload_size(request: Request, call_next):
    content_length = request.headers.get("content-length")

    if content_length and int(content_length) > 1024:  # 1 KB limit
        raise HTTPException(
            status_code=413,
            detail="Payload too large"
        )
    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"latency={duration:.3f}s"
    )

    return response

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    now = time.time()

    requests_by_ip[ip] = [t for t in requests_by_ip[ip] if now - t < WINDOW]

    if len(requests_by_ip[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    requests_by_ip[ip].append(now)
    return await call_next(request)

@app.get("/")
def root():
    return {
        "service": "SentinelPM",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "service": "SentinelPM",
        "status": "ok",
        "checks": {
            "api": "ok"
        }
    }

@app.post("/predict")
def predict(data: SensorInput):
    result = predict_health(
        data.temperature,
        data.vibration,
        data.voltage
    )

    external_response = explain_decision(result)
    logger.info(
        "Decision Generated",
        extra={"status": external_response["status"]}
    )

    return external_response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning(
        "Validation Failed",
        extra={
            "endpoint": request.url.path,
            "error_count": len(exc.errors())
        }
    )

    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request format"}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Service temporarily unavailable"}
    )