# brain.py
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

def decide_action(task, screen_content):
    response = llm.invoke(f"""
    You are a desktop AI agent.
    
    User wants to: {task}
    Current screen shows: {screen_content}
    
    Decide the single next action to take.
    Reply with JSON only:
    {{
        "action": "click" | "type" | "navigate" | "scroll" | "ask_user",
        "target": "description of element to find or URL or text to type",
        "reason": "why this action"
    }}
    """)
    
    import json
    return json.loads(response.content)