from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


class UnsupportedFileTypeError(ValueError):
    """Raised when a file's extension isn't one we can ingest."""


def load_pdf(path: Path) -> list[Document]:
    path = Path(path)
    reader = PdfReader(path)

    docs = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue  # image-only slides are expected in decks
        docs.append(
            Document(
                page_content=text,
                metadata={"source": path.name, "page": page_num},
            )
        )

    if not docs:
        raise ValueError(
            f"No extractable text in {path.name}; it may be a scanned PDF needing OCR."
        )
    return docs


def load_text(path: Path) -> list[Document]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        raise ValueError(f"{path.name} is empty")

    return [Document(page_content=text, metadata={"source": path.name, "page": 1})]


def load_document(path: Path) -> list[Document]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    elif suffix == ".txt":
        return load_text(path)
    else:
        raise UnsupportedFileTypeError(
            f"Unsupported file type: {path.suffix}. Only .pdf and .txt are supported."
        )


def clean_text(text: str) -> str:
    


def chunk_documents(docs, chunk_size: int, chunk_overlap: int) -> list[Document]: ...
def ingest_file(
    path: Path, *, document_id: str, user_id: str, chunk_size: int, chunk_overlap: int
) -> list[Document]: ...
