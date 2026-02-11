# chatbot.py

from llm_client import call_llm
from prompt import get_system_message
from memory import MemoryManager

class ChatBot:
    def __init__(self):
        self.memory = MemoryManager()

    def reply(self, user_input):
        messages = [
            get_system_message(),
            *self.memory.get_context(),
            {"role": "user", "content": user_input}
        ]

        response = call_llm(messages)
        self.memory.add_turn(user_input, response)

        return response

    def shutdown(self):
        self.memory.save()
