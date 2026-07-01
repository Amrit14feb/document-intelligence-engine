import fitz
import json
import os

from schemas.document_schemas import DOCUMENT

# ---------- PDF PATH ----------

pdf_path="data/pdfs/sample.pdf"

# ---------- OPEN PDF ----------

doc=fitz.open(pdf_path)

# ---------- CREATE DOCUMENT ----------

document=DOCUMENT.copy()

document["doc_id"]="DOC001"

document["source_file"]=os.path.basename(pdf_path)

# ---------- METADATA ----------

metadata=doc.metadata

document["title"]=metadata.get("title","Unknown Title")

document["metadata"]={

    "author":metadata.get("author","Unknown"),

    "producer":metadata.get("producer","Unknown"),

    "creation_date":metadata.get("creationDate","Unknown")
}

# ---------- PAGE LOOP ----------

for page_num in range(len(doc)):

    page=doc.load_page(page_num)

    text=page.get_text("text")

    page_object={

        "page_number":page_num+1,

        "raw_text":text,

        "char_count":len(text)
    }

    document["pages"].append(page_object)

# ---------- SAVE JSON ----------

output_path="data/extracted/extracted_document.json"

with open(output_path,"w",encoding="utf-8") as f:

    json.dump(

        document,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nEXTRACTION COMPLETE\n")

print(f"Pages extracted: {len(document['pages'])}")

print(f"Title: {document['title']}")

print("\nSaved to:")

print(output_path)