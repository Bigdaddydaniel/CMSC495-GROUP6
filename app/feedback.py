_FEEDBACK: list[dict] = []


def save_feedback(conversation_id: str, helpful: bool, comment: str | None) -> dict:
    record = {
        "conversation_id": conversation_id,
        "helpful": helpful,
        "comment": comment,
    }
    _FEEDBACK.append(record)
    return record
