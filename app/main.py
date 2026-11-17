from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .ai import GroundedSupportAI
from .conversations import add_message, create_conversation, get_history
from .feedback import save_feedback
from .models import ChatRequest, ChatResponse, FeedbackRequest
from .tickets import create_ticket, list_tickets

app = FastAPI(title="Group 6 Customer Service Alpha", version="0.1.0")
ai = GroundedSupportAI()


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <html><head><title>Group 6 Alpha</title></head>
    <body style='font-family:Arial;max-width:760px;margin:40px auto'>
      <h1>AI Customer Service Platform - Alpha</h1>
      <p>This prototype demonstrates grounded FAQ retrieval and automatic human handoff.</p>
      <p>Use <a href='/docs'>/docs</a> to test the API.</p>
      <h3>Team Roles</h3>
      <ul>
        <li>Ethan Scampone - Lead Architect</li>
        <li>Tanvi Gupta - Interface Designer</li>
        <li>Daniel Sandoval - Integration Lead</li>
      </ul>
    </body></html>
    """


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "release": "alpha"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    conversation_id = create_conversation()
    add_message(conversation_id, "customer", request.message)

    result = ai.answer(request.message)
    ticket_id = None
    status = "answered"

    if result.should_escalate:
        status = "escalated"
        ticket_id = create_ticket(
            request.customer_id,
            conversation_id,
            "AI confidence/policy required human review",
        )

    add_message(conversation_id, "assistant", result.answer)
    return ChatResponse(
        conversation_id=conversation_id,
        status=status,
        answer=result.answer,
        confidence=round(result.confidence, 3),
        source=result.source,
        ticket_id=ticket_id,
    )


@app.get("/conversations/{conversation_id}")
def conversation_history(conversation_id: str) -> dict:
    history = get_history(conversation_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conversation_id, "messages": history}


@app.post("/feedback")
def feedback(request: FeedbackRequest) -> dict:
    if get_history(request.conversation_id) is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"saved": True, "feedback": save_feedback(request.conversation_id, request.helpful, request.comment)}


@app.get("/tickets")
def tickets() -> dict:
    return {"tickets": list_tickets()}
