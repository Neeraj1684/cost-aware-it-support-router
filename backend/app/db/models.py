from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TicketLog(SQLModel, table=True):
    __tablename__ = "ticket_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str
    body: str
    engine: str         
    assigned_queue: str  
    confidence_score: float
    latency_ms: float
    llm_used: bool
    tokens_used: int
    cost_usd: float
    created_at: datetime = Field(default_factory=datetime.utcnow)