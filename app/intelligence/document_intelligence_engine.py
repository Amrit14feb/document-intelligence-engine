from app.extraction.pdf_parser import extract_pdf

from app.normalization.text_normalizer import normalize_document

from app.normalization.chunk_engine import build_chunks

from app.embeddings.embedder import generate_embeddings

from app.knowledge_extraction.relationship_extractor import extract_knowledge

from app.intelligence.summary_generator import generate_summary

from app.intelligence.structured_report_generator import generate_structured_report

from app.exporters.docx_exporter import export_report

from app.exporters.pdf_exporter import export_pdf

def run_document_pipeline(pdf_path):

    print("\n========== DOCUMENT INTELLIGENCE ENGINE ==========\n")