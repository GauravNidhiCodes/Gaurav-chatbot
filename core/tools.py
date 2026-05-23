from langchain_core.tools import tool

from core.retriever import retrieve_context


@tool
def search_knowledge_base(query: str):
    return retrieve_context(query)