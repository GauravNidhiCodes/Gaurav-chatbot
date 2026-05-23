from dataclasses import dataclass
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.file_loader import load_file_content

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
UPLOADS_DIR = BASE_DIR / "uploads"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=180,
)


@dataclass
class Chunk:
    source: str
    text: str
    is_upload: bool = False


def load_documents():
    documents = []

    for folder in (KNOWLEDGE_DIR, UPLOADS_DIR):
        if not folder.exists():
            continue

        for path in folder.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix.lower() not in {".txt", ".md", ".pdf", ".docx"}:
                continue

            try:
                text = load_file_content(path)
            except Exception:
                continue

            text = text.strip()
            if not text:
                continue

            documents.append(
                {
                    "source": str(path.relative_to(BASE_DIR)),
                    "text": text,
                    "is_upload": path.parent == UPLOADS_DIR,
                }
            )

    return documents


def build_index():
    raw_docs = load_documents()

    chunks = []

    for item in raw_docs:
        pieces = splitter.split_text(item["text"])

        for piece in pieces:
            cleaned = piece.strip()
            if cleaned:
                chunks.append(
                    Chunk(
                        source=item["source"],
                        text=cleaned,
                        is_upload=item["is_upload"],
                    )
                )

    texts = [chunk.text for chunk in chunks]

    if not texts:
        return [], None, None

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)

    return chunks, vectorizer, matrix


CHUNKS, VECTORIZER, MATRIX = build_index()


def refresh_index():
    global CHUNKS, VECTORIZER, MATRIX
    CHUNKS, VECTORIZER, MATRIX = build_index()


def _uploaded_chunks():
    return [chunk for chunk in CHUNKS if chunk.is_upload]


def retrieve_context(query, k=4):
    query = (query or "").strip().lower()

    if not query or not CHUNKS or VECTORIZER is None or MATRIX is None:
        return ""

    upload_chunks = _uploaded_chunks()

    if any(
        word in query
        for word in (
            "summarize",
            "summary",
            "uploaded",
            "pdf",
            "document",
            "file",
            "explain this",
            "what is this",
        )
    ):
        if upload_chunks:
            return "\n\n---\n\n".join(
                f"Source: {chunk.source}\n{chunk.text}"
                for chunk in upload_chunks[:k]
            )

    query_vector = VECTORIZER.transform([query])
    scores = cosine_similarity(query_vector, MATRIX).ravel()
    top_indices = scores.argsort()[::-1][:k]

    blocks = []

    for idx in top_indices:
        score = scores[idx]
        if score <= 0:
            continue

        chunk = CHUNKS[idx]
        blocks.append(
            f"Source: {chunk.source}\n{chunk.text}"
        )

    if blocks:
        return "\n\n---\n\n".join(blocks)

    if upload_chunks:
        return "\n\n---\n\n".join(
            f"Source: {chunk.source}\n{chunk.text}"
            for chunk in upload_chunks[:k]
        )

    return ""