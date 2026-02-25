from app.config import TEMP_THRESHOLD, VIBRATION_THRESHOLD, VOLTAGE_MAX, VOLTAGE_MIN


def predict_health(temperature: float, vibration: float, voltage: float):
    risk = 0.0
       
    if temperature > TEMP_THRESHOLD:
        risk += 0.4
    if vibration > VIBRATION_THRESHOLD:
        risk += 0.4
    if voltage < VOLTAGE_MIN or voltage > VOLTAGE_MAX:
        risk += 0.2

    health = "faulty" if risk >= 0.5 else "healthy"

    return {
        "health": health,
        "risk_score": round(risk, 2)
    }
