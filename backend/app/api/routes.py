from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func


from backend.app.schemas import TicketRequest, RoutingResponse, TicketStatusUpdate, PaginatedTickets
from backend.app.dependencies import get_model_manager, get_current_user
from backend.app.services.predictor import predict_ticket
from backend.app.db.database import get_session
from backend.app.db.models import TicketLog, User
import traceback

router = APIRouter()

@router.post(
    "/api/v1/tickets/route",
    response_model=RoutingResponse
)
async def route_ticket(
    ticket: TicketRequest,
    manager = Depends(get_model_manager),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        result = predict_ticket(
            ticket.subject,
            ticket.body,
            manager
        )
    
        log_entry = TicketLog(
            subject=ticket.subject,
            body=ticket.body,
            engine=result["routing"]["engine"],
            assigned_queue=result["routing"]["queue"],
            confidence_score=result["routing"]["confidence"],
            latency_ms=result["metrics"]["latency_ms"],
            llm_used=result["metrics"]["llm_used"],
            tokens_used=result["metrics"]["tokens_used"],
            cost_usd=result["metrics"]["cost_usd"],
            user_id=current_user.id
        )

        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)

        return result
    
    except Exception as e:
        db.rollback()
        # --- NEW VISUAL ALARMS ---
        print("\n" + "!!!" * 15)
        print("CRITICAL ERROR IN ROUTE_TICKET:")
        traceback.print_exc()  # This prints the EXACT line number that crashed
        print("!!!" * 15 + "\n")
        # --------------------------
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

@router.get("/api/v1/tickets/logs", response_model=PaginatedTickets)
def get_ticket_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        count_statement = select(func.count(TicketLog.id))
        statement = select(TicketLog).order_by(TicketLog.created_at.desc()).offset(skip).limit(limit)
    else:
        count_statement = select(func.count(TicketLog.id)).where(TicketLog.user_id == current_user.id)
        statement = select(TicketLog).where(TicketLog.user_id == current_user.id).order_by(TicketLog.created_at.desc()).offset(skip).limit(limit)

    total_count = db.exec(count_statement).one()
    logs = db.exec(statement).all()
    return {
        "items": logs,
        "total": total_count
    }

@router.patch("/api/v1/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status_update: TicketStatusUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to resolve tickets")
    
    ticket = db.get(TicketLog, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = status_update.status
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket

@router.get("/")
def root():
    return {
        "message": "Cost-Aware IT Support Router is running!"
    }

