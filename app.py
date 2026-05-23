import shutil
import traceback
from pathlib import Path

import gradio as gr

from core.agent import ask_agent
from core.retriever import refresh_index

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


def get_path(file):
    if isinstance(file, str):
        return Path(file)
    if hasattr(file, "name"):
        return Path(file.name)
    if hasattr(file, "path"):
        return Path(file.path)
    return Path(str(file))


def upload_files(files):
    if not files:
        return "No files uploaded."

    if not isinstance(files, list):
        files = [files]

    uploaded = []

    for file in files:
        source = get_path(file)

        if not source.exists():
            continue

        destination = UPLOADS_DIR / source.name
        shutil.copy2(source, destination)
        uploaded.append(source.name)

    refresh_index()

    if not uploaded:
        return "No valid files were uploaded."

    return "Uploaded: " + ", ".join(uploaded)


def respond(message, history):
    history = history or []
    message = (message or "").strip()

    if not message:
        return "", history

    try:
        answer = ask_agent(message, history)
    except Exception as e:
        traceback.print_exc()
        answer = f"Error: {str(e)}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return "", history


with gr.Blocks() as demo:
    gr.Markdown("# Gaurav AI")
    gr.Markdown("LangChain + OpenRouter + RAG")

    with gr.Row():
        uploader = gr.File(
            file_count="multiple",
            type="filepath",
            label="Upload Files",
        )
        upload_button = gr.Button("Upload")

    upload_status = gr.Textbox(label="Upload Status", interactive=False)

    upload_button.click(
        upload_files,
        inputs=uploader,
        outputs=upload_status,
    )

    chatbot = gr.Chatbot(
        height=520,
        value=[],
        label="Chatbot",
    )

    message = gr.Textbox(
        placeholder="Ask something...",
        label="Message",
    )

    clear = gr.Button("Clear")

    message.submit(
        respond,
        inputs=[message, chatbot],
        outputs=[message, chatbot],
    )

    clear.click(
        lambda: ("", []),
        outputs=[message, chatbot],
    )

if __name__ == "__main__":
    demo.launch()