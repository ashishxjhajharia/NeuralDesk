
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np


def extract_pdf_text(pdf_path):
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


# Step 1: Read the PDF.
pdf_path = input("Enter PDF path: ").strip()
pages = extract_pdf_text(pdf_path)

# Step 2: Create chunks and preserve their page numbers.
documents = []

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk_number, chunk in enumerate(chunks, start=1):
        documents.append({
            "page": page["page"],
            "chunk": chunk_number,
            "text": chunk,
        })

print(f"\nPrepared {len(documents)} chunks.")

# Step 3: Load our embedding model.
print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu",
)

# Step 4: Convert every chunk into a vector.
texts = [document["text"] for document in documents]

document_vectors = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=True,
)

print("Embedding matrix shape:", document_vectors.shape)

# Step 5: Get a question from the user.
query = input("\nAsk a question about the PDF: ").strip()

# Step 6: Convert the question into a vector.
query_vector = model.encode(
    [query],
    normalize_embeddings=True,
)[0]

# Step 7: Calculate similarity with every chunk.
scores = document_vectors @ query_vector

# Step 8: Find the five highest-scoring chunks.
top_k = min(5, len(documents))
best_indices = np.argsort(scores)[::-1][:top_k]

# Step 9: Display the results.
print("\n--- Most Relevant Passages ---")

for rank, index in enumerate(best_indices, start=1):
    document = documents[int(index)]

    print(f"\nRank: {rank}")
    print(f"Similarity: {float(scores[index]):.4f}")
    print(f"Page: {document['page']}")
    print(f"Chunk: {document['chunk']}")
    print(document["text"])
