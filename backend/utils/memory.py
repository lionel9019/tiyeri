# backend/utils/memory.py
import os
import json

CHAT_MEMORY_FILE = "chat_memory.json"

def load_chat_memory():
    if os.path.exists(CHAT_MEMORY_FILE):
        with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_chat_memory(data):
    with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
