import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

from core.memory import history_to_messages
from core.prompts import PROMPT
from core.retriever import retrieve_context

load_dotenv()

MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

llm = ChatOpenRouter(
    model=MODEL,
    temperature=0.2,
)

chain = PROMPT | llm


def ask_agent(question: str, history=None):
    context = retrieve_context(question)
    messages = history_to_messages(history)

    result = chain.invoke(
        {
            "history": messages,
            "context": context,
            "question": question,
        }
    )

    return result.content.strip()