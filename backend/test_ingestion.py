from backend.app.ingestion.document_loader import load_document

file_path = "data/raw/attention_paper.pdf"

documents = load_document(file_path)

print("Total pages extracted:", len(documents))

for document in documents:

    text = document["text"]
    metadata = document["metadata"]

    print("\n" + "=" * 60)

    print("SOURCE:", metadata["source"])
    print("PAGE:", metadata["page_number"])
    print("CHARACTERS:", len(text))

    print("\nEXTRACTED TEXT:")
    print(text[:500])