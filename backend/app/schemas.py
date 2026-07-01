from pydantic import BaseModel

class TicketRequest(BaseModel):
    subject: str
    body: str

class RoutingInfo(BaseModel):
    engine: str
    queue: str
    confidence: float

class Metrics(BaseModel):
    latency_ms: float
    llm_used: bool
    cost_usd: float
    tokens_used: int

class RoutingResponse(BaseModel):
    routing: RoutingInfo
    metrics: Metrics