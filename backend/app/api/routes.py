from fastapi import APIRouter, Depends

from backend.app.schemas import TicketRequest, RoutingResponse
from backend.app.dependencies import get_model_manager
from backend.app.services.predictor import predict_ticket

router = APIRouter()

@router.post(
    "/api/v1/tickets/route",
    response_model=RoutingResponse
)
async def route_ticket(
    ticket: TicketRequest,
    manager = Depends(get_model_manager)
):
    return predict_ticket(
        ticket.subject,
        ticket.body,
        manager
    )

@router.get("/")
def root():
    return {
        "message": "Cost-Aware IT Support Router is running!"
    }

