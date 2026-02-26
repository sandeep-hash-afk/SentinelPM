from fastapi import FastAPI, Request, HTTPException
from app.models import SensorInput
from app.services import predict_health
import logging
import time
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.decision_layer import explain_decision

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


@app.get("/")
def root():
    return {
        "service": "SentinelPM",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

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