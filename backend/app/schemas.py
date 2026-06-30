from pydantic import BaseModel

class TicketRequest(BaseModel):
    subject: str
    body: str

class RoutingResponse(BaseModel):
    routed_by: str
    assigned_queue: str
    confidence_score: float
    cost_incurred: str
    latency_ms: float
    requires_human_review: bool