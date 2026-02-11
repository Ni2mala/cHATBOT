# memory.py

import json
from config import MAX_SHORT_MEMORY, MEMORY_FILE

class MemoryManager:
    def __init__(self):
        self.short_memory = []

    def add_turn(self, user_msg, bot_msg):
        self.short_memory.append({"role": "user", "content": user_msg})
        self.short_memory.append({"role": "assistant", "content": bot_msg})

        # keep last N turns (not messages)
        while len(self.short_memory) > MAX_SHORT_MEMORY * 2:
            self.short_memory.pop(0)

    def get_context(self):
        return list(self.short_memory)

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.short_memory, f, indent=2)
