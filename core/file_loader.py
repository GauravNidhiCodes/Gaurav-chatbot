from pathlib import Path

from docx import Document
from pypdf import PdfReader


def load_text_file(path):
    return Path(path).read_text(
        encoding="utf-8",
        errors="ignore",
    )


def load_pdf_file(path):

    reader = PdfReader(path)

    text = []

    for page in reader.pages:
        content = page.extract_text()

        if content:
            text.append(content)

    return "\n".join(text)


def load_docx_file(path):

    document = Document(path)

    text = []

    for para in document.paragraphs:
        value = para.text.strip()

        if value:
            text.append(value)

    return "\n".join(text)


def load_file_content(path):

    suffix = Path(path).suffix.lower()

    if suffix == ".txt":
        return load_text_file(path)

    if suffix == ".md":
        return load_text_file(path)

    if suffix == ".pdf":
        return load_pdf_file(path)

    if suffix == ".docx":
        return load_docx_file(path)

    return ""