def predict_health(temperature: float, vibration: float, voltage: float):
    risk = 0.0
       
    if temperature > 80:
        risk += 0.4
    if vibration > 70:
        risk += 0.4
    if voltage < 200 or voltage > 240:
        risk += 0.2

    health = "faulty" if risk >= 0.5 else "healthy"

    return {
        "health": health,
        "risk_score": round(risk, 2)
    }
