

import os
from copy import deepcopy

import gradio as gr
from dotenv import load_dotenv
from openai import (
    OpenAI,
    AuthenticationError,
    APITimeoutError,
    APIConnectionError,
    APIError,
)

from rag import (
    search_knowledge,
    format_context,
)

# Load environment variables
load_dotenv()

# Model
MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/auto"
)

# System prompt
SYSTEM_PROMPT = """
You are a RAG assistant.

You MUST answer from the provided knowledge base context whenever relevant.

If the answer exists in the context:
- answer directly
- do not ask for more context
- do not say "as of my last update"
- do not refuse

Always prioritize the provided context over your internal knowledge.
""".strip()

# OpenRouter API key
api_key = os.getenv("OPENAI_API_KEY")

# OpenRouter client
client = (
    OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )
    if api_key
    else None
)


def build_messages(
    history,
    user_message,
    rag_context=""
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Inject RAG context
    if rag_context:

        messages.append(
            {
                "role": "system",
                "content": f"""
Relevant knowledge base context:

{rag_context}

Use this information as the primary source of truth.
""",
            }
        )

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    return messages


def respond(message, history):

    message = (message or "").strip()

    history = history or []

    if not message:
        return "", history, history

    # Missing API key
    if client is None:

        new_history = history + [
            {
                "role": "user",
                "content": message,
            },
            {
                "role": "assistant",
                "content": (
                    "OpenRouter API key "
                    "not found in .env file."
                ),
            },
        ]

        snapshot = deepcopy(new_history)

        return "", snapshot, snapshot

    # RAG retrieval
    hits = search_knowledge(message)

    rag_context = format_context(hits)

    print("\n========== RAG CONTEXT ==========")
    print(rag_context)
    print("=================================\n")

    messages = build_messages(
        history,
        message,
        rag_context,
    )

    try:

        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            temperature=0.1,
            timeout=30.0,
        )

        new_history = history + [
            {
                "role": "user",
                "content": message,
            },
            {
                "role": "assistant",
                "content": "",
            },
        ]

        snapshot = deepcopy(new_history)

        yield "", snapshot, snapshot

        response_text = ""

        for chunk in stream:

            content = (
                chunk.choices[0]
                .delta
                .content
                if chunk.choices
                else None
            )

            if content:

                response_text += content

                new_history[-1]["content"] = (
                    response_text
                )

                snapshot = deepcopy(new_history)

                yield "", snapshot, snapshot

    except AuthenticationError:

        error_text = (
            "Invalid OpenRouter API key."
        )

    except APITimeoutError:

        error_text = "Request timed out."

    except APIConnectionError:

        error_text = (
            "Failed to connect to OpenRouter."
        )

    except APIError as e:

        error_text = (
            f"API Error: {str(e)}"
        )

    except Exception as e:

        error_text = (
            f"Unexpected Error: {str(e)}"
        )

    else:
        return

    new_history = history + [
        {
            "role": "user",
            "content": message,
        },
        {
            "role": "assistant",
            "content": error_text,
        },
    ]

    snapshot = deepcopy(new_history)

    yield "", snapshot, snapshot


with gr.Blocks() as demo:

    gr.Markdown(
        """
        # AI Chatbot

        A chatbot built with:
        - Gradio
        - OpenRouter
        - Lightweight RAG
        """
    )

    chatbot = gr.Chatbot(
        height=500
    )

    state = gr.State([])

    message_box = gr.Textbox(
        placeholder=(
            "Type your message "
            "and press Enter..."
        ),
        label="Message",
    )

    with gr.Row():

        send_button = gr.Button(
            "Send",
            variant="primary",
        )

        clear_button = gr.Button(
            "Clear"
        )

    # Enter submit
    message_box.submit(
        respond,
        inputs=[
            message_box,
            state,
        ],
        outputs=[
            message_box,
            chatbot,
            state,
        ],
    )

    # Button submit
    send_button.click(
        respond,
        inputs=[
            message_box,
            state,
        ],
        outputs=[
            message_box,
            chatbot,
            state,
        ],
    )

    # Clear chat
    clear_button.click(
        lambda: ("", [], []),
        outputs=[
            message_box,
            chatbot,
            state,
        ],
    )

# Launch
if __name__ == "__main__":

    demo.launch(
        share=True
    )