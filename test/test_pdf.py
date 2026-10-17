
from pypdf import PdfReader

print("NeuralDesk PDF text extraction test")

pdf_path = input("Enter the path to a PDF file: ").strip()

reader = PdfReader(pdf_path)

print("Number of pages:", len(reader.pages))

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""

    print(f"\n--- Page {page_number} ---")
    print(text[:1000])
