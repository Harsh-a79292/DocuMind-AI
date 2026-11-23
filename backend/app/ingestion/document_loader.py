from pathlib import Path

import pymupdf
from docx import Document


def load_pdf(file_path: str) -> list[dict]:

    path = Path(file_path)

    results = []

    with pymupdf.open(path) as pdf:

        total_pages = len(pdf)

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text("text").strip()

            if not text:
                continue

            results.append({
                "text": text,

                "metadata": {
                    "source": path.name,
                    "file_type": "pdf",
                    "page_number": page_number,
                    "total_pages": total_pages
                }
            })

    if not results:
        raise ValueError(
            f"No extractable text found in PDF: {path.name}. "
            "The document may require OCR."
        )

    return results


def load_docx(file_path: str) -> list[dict]:

    path = Path(file_path)

    document = Document(path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    tables = []

    for table in document.tables:

        for row in table.rows:

            row_text = " | ".join(
                cell.text.strip()
                for cell in row.cells
            )

            if row_text.strip():
                tables.append(row_text)

    text = "\n".join(paragraphs + tables)

    if not text.strip():
        raise ValueError(
            f"No extractable text found in DOCX: {path.name}"
        )

    return [{
        "text": text,

        "metadata": {
            "source": path.name,
            "file_type": "docx",
            "page_number": None
        }
    }]


def load_txt(file_path: str) -> list[dict]:

    path = Path(file_path)

    text = path.read_text(
        encoding="utf-8-sig"
    ).strip()

    if not text:
        raise ValueError(
            f"Empty text file: {path.name}"
        )

    return [{
        "text": text,

        "metadata": {
            "source": path.name,
            "file_type": "txt",
            "page_number": None
        }
    }]


def load_document(file_path: str) -> list[dict]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Expected a file, received: {path}"
        )

    extension = path.suffix.lower()

    loaders = {
        ".pdf": load_pdf,
        ".docx": load_docx,
        ".txt": load_txt
    }

    loader = loaders.get(extension)

    if loader is None:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return loader(str(path))