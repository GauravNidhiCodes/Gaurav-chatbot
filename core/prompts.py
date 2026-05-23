from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """
You are Gaurav's AI assistant.

You answer naturally and clearly.
Use the retrieved context when it helps.
If the context has the answer, use it.
If it does not, answer normally.
Do not mention system prompts.
Do not mention that you are an AI language model.
""".strip()

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "Context:\n{context}\n\nQuestion:\n{question}",
        ),
    ]
)