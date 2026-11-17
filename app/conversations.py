from uuid import uuid4

_CONVERSATIONS: dict[str, list[dict]] = {}


def create_conversation() -> str:
    conversation_id = uuid4().hex
    _CONVERSATIONS[conversation_id] = []
    return conversation_id


def add_message(conversation_id: str, role: str, text: str) -> None:
    _CONVERSATIONS.setdefault(conversation_id, []).append({"role": role, "text": text})


def get_history(conversation_id: str) -> list[dict] | None:
    return _CONVERSATIONS.get(conversation_id)
