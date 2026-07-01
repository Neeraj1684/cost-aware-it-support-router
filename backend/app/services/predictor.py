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
        return {
            "routing": {
                "engine": "Machine Learning",
                "queue": CATEGORY_MAP[predicted_cluster],
                "confidence": round(confidence, 4)
            },
            "metrics": {
                "latency_ms": latency,
                "llm_used": False,
                "cost_usd": 0.0,
                "tokens_used": 0
            }
        }
    
    return {
        "routing": {
            "engine": "LLM Fallback",
            "queue": "Pending LLM Analysis",
            "confidence": round(confidence, 4)
        },
        "metrics": {
            "latency_ms": latency,
            "llm_used": True,
            "cost_usd": 0.0,
            "tokens_used": 0
        }
    }