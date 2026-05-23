from langchain_core.messages import AIMessage, HumanMessage


def history_to_messages(history):
    messages = []

    for item in history or []:
        if isinstance(item, dict):
            role = item.get("role")
            content = (item.get("content") or "").strip()

            if not content:
                continue

            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_text, assistant_text = item

            if user_text:
                messages.append(HumanMessage(content=str(user_text)))

            if assistant_text:
                messages.append(AIMessage(content=str(assistant_text)))

    return messages