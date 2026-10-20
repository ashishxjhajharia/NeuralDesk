
from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    """Extract and clean text from every PDF page."""
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())

        pages.append({
            "page": page_number,
            "text": text,
        })

    return pages


def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping character-based chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


pdf_path = input("Enter PDF path: ").strip()
pages = extract_pdf_text(pdf_path)

all_chunks = []

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk_number, chunk in enumerate(chunks, start=1):
        all_chunks.append({
            "page": page["page"],
            "chunk": chunk_number,
            "text": chunk,
        })

print("\nPages extracted:", len(pages))
print("Total chunks:", len(all_chunks))

for item in all_chunks[:3]:
    print(f"\nPage {item['page']}, chunk {item['chunk']}:")
    print(item["text"])
