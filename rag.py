

from dataclasses import dataclass
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)

from sklearn.metrics.pairwise import (
    cosine_similarity,
)

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_DIR = (
    BASE_DIR / "knowledge"
)

CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
TOP_K = 4
MIN_SCORE = 0.08


@dataclass
class Chunk:

    source: str
    text: str


def chunk_text(
    text: str,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP,
):

    text = " ".join(
        (text or "").split()
    )

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text),
        )

        chunks.append(
            text[start:end]
        )

        if end == len(text):
            break

        start = max(
            0,
            end - overlap,
        )

    return chunks


def load_chunks():

    chunks = []

    if not KNOWLEDGE_DIR.exists():
        return chunks

    for path in sorted(
        KNOWLEDGE_DIR.rglob("*")
    ):

        if (
            path.suffix.lower()
            not in {
                ".txt",
                ".md",
            }
        ):
            continue

        try:

            raw_text = (
                path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            )

        except Exception:
            continue

        for idx, part in enumerate(
            chunk_text(raw_text),
            start=1,
        ):

            chunks.append(
                Chunk(
                    source=(
                        f"{path.name}"
                        f" · chunk {idx}"
                    ),
                    text=part,
                )
            )

    return chunks


def search_knowledge(
    query: str
):

    query = (
        query or ""
    ).strip()

    if not query:
        return []

    chunks = load_chunks()

    print(
        f"\nLoaded "
        f"{len(chunks)} "
        f"chunks\n"
    )

    if not chunks:
        return []

    corpus = [
        c.text
        for c in chunks
    ]

    vectorizer = (
        TfidfVectorizer(
            stop_words="english"
        )
    )

    matrix = (
        vectorizer.fit_transform(
            corpus
        )
    )

    query_vector = (
        vectorizer.transform(
            [query]
        )
    )

    scores = cosine_similarity(
        query_vector,
        matrix,
    ).flatten()

    ranked_indices = (
        scores.argsort()[::-1]
    )

    results = []

    for idx in ranked_indices[:TOP_K]:

        score = float(scores[idx])

        if score < MIN_SCORE:
            continue

        results.append(
            {
                "source": (
                    chunks[idx]
                    .source
                ),
                "text": (
                    chunks[idx]
                    .text
                ),
                "score": (
                    f"{score:.2f}"
                ),
            }
        )

    return results


def format_context(results):

    if not results:
        return ""

    blocks = []

    for item in results:

        blocks.append(
            f"Source: "
            f"{item['source']}\n\n"
            f"{item['text']}"
        )

    return "\n\n---\n\n".join(
        blocks
    )