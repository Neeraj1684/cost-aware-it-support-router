import numpy as np
import time
from backend.app.constants import CATEGORY_MAP, CONFIDENCE_THRESHOLD


def predict_ticket(subject, body, manager):
    
    start_time = time.time()

    combined_text = f"Subject: {subject} | Body: {body}"

    vector = manager.embedder.encode([combined_text])

    probabilities = manager.router_model.predict_proba(vector)[0]

    confidence = float(np.max(probabilities))

    predicted_cluster = int(np.argmax(probabilities))

    latency = round((time.time() - start_time) * 1000, 2)

    if confidence >= CONFIDENCE_THRESHOLD:
        return{
            "routed_by": "Machine Learning",
            "assigned_queue": CATEGORY_MAP[predicted_cluster],
            "confidence_score": round(confidence, 4),
            "cost_incurred": "Rs. 0.00",
            "latency_ms": latency,
            "requires_human_review": False
        }
    
    return {
        "routed_by": "LLM Fallback",
        "assigned_queue": "Pending LLM Analysis",
        "confidence_score": round(confidence, 4),
        "cost_incurred": "Calculating...",
        "latency_ms": latency,
        "requires_human_review": True
    }