from pydantic import BaseModel, Field, Extra

class SensorInput(BaseModel):
    temperature: float = Field(..., ge=40, le=150)
    vibration: float = Field(..., ge=0, le=200)
    voltage: float = Field(..., ge=0, le=500)

    model_config = {
         "extra": "forbid"
    }