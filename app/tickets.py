from uuid import uuid4

_TICKETS: dict[str, dict] = {}


def create_ticket(customer_id: str, conversation_id: str, reason: str) -> str:
    ticket_id = f"TKT-{uuid4().hex[:8].upper()}"
    _TICKETS[ticket_id] = {
        "customer_id": customer_id,
        "conversation_id": conversation_id,
        "reason": reason,
        "status": "open",
    }
    return ticket_id


def list_tickets() -> list[dict]:
    return [{"ticket_id": key, **value} for key, value in _TICKETS.items()]
