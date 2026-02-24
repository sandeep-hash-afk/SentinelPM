def explain_decision(internal_result: dict):
    health = internal_result["health"]
    risk_score = internal_result["risk_score"]

    if risk_score >= 0.7:
        confidence = "High"
        action = "Immediate inspection recommended"
    elif risk_score >= 0.5:
        confidence = "Medium"
        action = "Schedule maintenance soon"
    else:
        confidence = "Low"
        action = "Continue monitoring"

    if health == "faulty":
        status = "Fault detected"
        reason = "Abnormal sensor readings observed"
    else:
        status = "System healthy"
        reason = "All readings within normal range"

    return {
        "status": status,
        "reason": reason,
        "confidence_level": confidence,
        "recommended_action": action
    }