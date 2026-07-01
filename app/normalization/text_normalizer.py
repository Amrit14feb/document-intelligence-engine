import json
import re

# ---------- LOAD EXTRACTED DATA ----------

with open(
    "data/extracted/extracted_document.json",
    "r",
    encoding="utf-8"
) as f:

    document=json.load(f)

# ---------- NORMALIZATION FUNCTION ----------

def clean_text(text):

    # remove extra spaces

    text=re.sub(r"\s+"," ",text)

    # remove repeated newlines

    text=re.sub(r"\n+","\n",text)

    # trim edges

    text=text.strip()

    return text

# ---------- NORMALIZE PAGES ----------

normalized_pages=[]

for page in document["pages"]:

    cleaned=clean_text(page["raw_text"])

    normalized_pages.append({

        "page_number":page["page_number"],

        "clean_text":cleaned,

        "char_count":len(cleaned)
    })

# ---------- SAVE OUTPUT ----------

normalized_document={

    "doc_id":document["doc_id"],

    "title":document["title"],

    "pages":normalized_pages
}

with open(
    "data/normalized/normalized_document.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        normalized_document,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nNORMALIZATION COMPLETE\n")

print(
    f"Pages normalized: {len(normalized_pages)}"
)