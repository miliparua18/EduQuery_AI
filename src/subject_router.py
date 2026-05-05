from src.model import get_gemini_model
from langchain_core.messages import SystemMessage, HumanMessage
from Prompts.subject_router_prompt import SYSTEM_PROMPT

router_llm = get_gemini_model()

def detect_subject(query: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Query: {query}")
    ]

    try:
        response = router_llm.invoke(messages)
        return response.text.strip()

    except Exception as e:
        print("Subject router error:", e)
        return "Unknown"