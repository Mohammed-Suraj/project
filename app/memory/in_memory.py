from typing import Any, Dict, List
from collections import defaultdict


class ChatMemory:
    _store: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    @classmethod
    def add_message(cls, session_id: str, role: str, content: Any) -> None:
        cls._store[session_id].append({"role": role, "content": content})

    @classmethod
    def get_history(cls, session_id: str) -> List[Dict[str, Any]]:
        return cls._store.get(session_id, [])

    @classmethod
    def reset(cls, session_id: str) -> None:
        cls._store.pop(session_id, None)