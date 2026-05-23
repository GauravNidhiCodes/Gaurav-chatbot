# Gaurav AI

Gaurav AI is a local chatbot built with **Gradio**, **LangChain**, **OpenRouter**, and **RAG**.  
It supports:

- Chat interface
- Multi-file upload
- PDF, TXT, MD, DOCX support
- Local knowledge retrieval
- OpenRouter-based model responses

## Features

- Clean Gradio UI
- OpenRouter integration
- Retrieval-Augmented Generation (RAG)
- Upload files and ask questions from them
- Works with local knowledge base
- Modular code structure

## Tech Stack

- Python
- Gradio
- LangChain
- OpenRouter
- scikit-learn
- python-dotenv
- pypdf
- python-docx

## Project Structure

```txt
Gaurav-chatbot/
├── app.py
├── requirements.txt
├── .env
├── core/
│   ├── __init__.py
│   ├── agent.py
│   ├── file_loader.py
│   ├── memory.py
│   ├── prompts.py
│   ├── retriever.py
│   └── tools.py
├── knowledge/
├── uploads/
└── vectorstore/