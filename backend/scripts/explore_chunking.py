import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def load_pdf(path: str | Path) -> list[Document]:
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


path = sys.argv[1] if len(sys.argv) > 1 else "data/samples/CS425 Week1 Introduction.pdf"
docs = load_pdf(path)

total_pages = len(PdfReader(path).pages)
print(f"{len(docs)} of {total_pages} pages have text")
print(docs[0].metadata)
print(docs[0].page_content[:300])

for chunk_size in (200, 800, 2000):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size // 10,
    )
    chunks = splitter.split_documents(docs)
    lengths = [len(c.page_content) for c in chunks]

    print(f"\n=== chunk_size={chunk_size} ===")
    print(
        f"{len(chunks)} chunks | avg {sum(lengths) // len(lengths)} chars "
        f"| min {min(lengths)} | max {max(lengths)}"
    )
    print(f"sample {chunks[1].metadata}:\n{chunks[1].page_content}")
