import time


class SessionMemory:
    def __init__(self, max_turns: int = 10, timeout_minutes: int = 30):
        # Store all sessions in a dictionary keyed by session_id
        self.sessions: dict[str, dict] = {}
        self.max_turns = max_turns
        self.timeout_seconds = timeout_minutes * 60

    def _is_expired(self, session_id: str) -> bool:
        # A session is expired if it doesn't exist or hasn't been active recently
        if session_id not in self.sessions:
            return True
        last_active = self.sessions[session_id]["last_active"]
        return (time.time() - last_active) > self.timeout_seconds

    def get_history(self, session_id: str) -> list[dict]:
        # Return conversation history, or empty list if session expired
        if self._is_expired(session_id):
            self.sessions.pop(session_id, None)
            return []
        return self.sessions[session_id]["history"]

    def add_turn(self, session_id: str, user_message: str, assistant_message: str):
        # Create a fresh session if this one expired or is new
        if self._is_expired(session_id):
            self.sessions[session_id] = {"history": [], "last_active": time.time()}

        # Append the new conversation turn
        self.sessions[session_id]["history"].append(
            {"user": user_message, "assistant": assistant_message}
        )
        self.sessions[session_id]["last_active"] = time.time()

        # Trim history to max_turns to keep memory bounded
        if len(self.sessions[session_id]["history"]) > self.max_turns:
            self.sessions[session_id]["history"] = self.sessions[session_id]["history"][
                -self.max_turns :
            ]
