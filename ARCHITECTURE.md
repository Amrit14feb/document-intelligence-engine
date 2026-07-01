# ARCHITECTURE

# Document Intelligence Engine Architecture

---

# Overview

The Document Intelligence Engine is built as a modular AI pipeline where each module has a single responsibility. Data flows sequentially through extraction, normalization, retrieval, reasoning, intelligence generation, and export.

The architecture is designed to be easily extensible without modifying existing modules.

---

# High-Level Architecture

```text
                         PDF
                          │
                          ▼
                PDF Extraction Layer
                          │
                          ▼
               Text Normalization Layer
                          │
                          ▼
                Semantic Chunking Layer
                          │
                          ▼
                Embedding Generation
                          │
                          ▼
                  ChromaDB Storage
                          │
        ┌─────────────────┴────────────────┐
        ▼                                  ▼
 Knowledge Extraction              Semantic Retrieval
        │                                  │
        ▼                                  │
 Knowledge Graph                           │
        │                                  │
        ▼                                  ▼
 Graph Retrieval                  Retrieved Chunks
        └──────────────┬───────────────────┘
                       ▼
                 Hybrid Ranking
                       ▼
                 Context Builder
                       ▼
                  GPT-4o-mini
                       ▼
          Document Intelligence Layer
                       ▼
              Summary / Report / QA
                       ▼
               DOCX / PDF Export
```

---

# Folder Responsibilities

## app/

Contains all application logic.

### extraction/

Responsible for extracting raw text from PDF documents.

Current modules:

* pdf_parser.py

Output:

* extracted_document.json

---

### normalization/

Responsible for cleaning extracted text and converting it into a normalized representation.

Modules

* text_normalizer.py
* chunk_engine.py

Output

* normalized_document.json
* chunked_document.json

---

### embeddings/

Generates vector embeddings for semantic retrieval.

Modules

* embedder.py

Uses

* Sentence Transformers
* all-MiniLM-L6-v2

Output

Stored vectors inside ChromaDB.

---

### retrieval/

Responsible for retrieving information.

Modules

* semantic_retriever.py
* graph_retriever.py
* graph_expansion.py
* hybrid_ranker.py
* entity_detector.py
* multi_entity_detector.py

Pipeline

Question

↓

Entity Detection

↓

Graph Expansion

↓

Semantic Retrieval

↓

Hybrid Ranking

↓

Relevant Context

---

### knowledge_extraction/

Builds structured knowledge.

Modules

* entity_extractor.py
* relationship_extractor.py
* concept_extractor.py
* knowledge_builder.py
* graph_cleaner.py

Outputs

entities.json

relationships.json

concepts.json

knowledge_graph.json

---

### reasoning/

Responsible for LLM reasoning.

Modules

* prompts.py
* context_builder.py
* rag_engine.py
* llm.py

Responsibilities

Prompt construction

Context fusion

GraphRAG

Question Answering

---

### intelligence/

Generates high-level outputs.

Modules

* summary_generator.py
* report_generator.py
* structured_report_generator.py

Outputs

Executive Summary

Technical Report

Structured Report

---

### exporters/

Responsible for exporting outputs.

Modules

* pdf_exporter.py
* docx_exporter.py

Supported formats

PDF

DOCX

---

### visualization/

Knowledge graph visualization.

---

# Data Flow

```text
PDF
 │
 ▼
Extraction
 │
 ▼
Normalization
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Vector Database
 │
 ▼
Knowledge Extraction
 │
 ▼
Knowledge Graph
 │
 ▼
Retrieval
 │
 ▼
Reasoning
 │
 ▼
Document Intelligence
 │
 ▼
Export
```

---

# Retrieval Architecture

The project implements Hybrid Retrieval.

## Semantic Retrieval

Purpose

Retrieve semantically similar chunks.

Technology

Sentence Transformers

ChromaDB

---

## Graph Retrieval

Purpose

Retrieve connected entities and relationships.

Technology

Knowledge Graph

---

## Hybrid Ranking

Purpose

Merge semantic retrieval and graph retrieval into one ranked context.

---

# Knowledge Graph

Current graph components

* Entities
* Relationships
* Concepts
* Entity Aliases

Future additions

* Confidence Scores
* Entity Types
* Weighted Relationships
* Community Detection

---

# Intelligence Layer

Current capabilities

* Question Answering
* Executive Summary
* Technical Report
* Structured Report

Future capabilities

* Literature Review
* Citation Generation
* Timeline Generation
* Table Understanding
* Diagram Understanding
* Multi-document Reports

---

# Design Principles

Every module should:

* Have one responsibility.
* Be independently testable.
* Avoid duplicated logic.
* Be reusable.
* Be loosely coupled.

---

# Development Guidelines

When adding a new feature:

1. Create a dedicated module.
2. Add unit tests in `tests/`.
3. Update README if needed.
4. Keep retrieval and reasoning separate.
5. Do not modify unrelated modules.

---

# Future Architecture

```text
Multiple PDFs
       │
       ▼
Document Index
       │
       ▼
Global Knowledge Graph
       │
       ▼
GraphRAG
       │
       ▼
Citation Engine
       │
       ▼
Research Assistant
       │
       ▼
Interactive Web Application
```

---

# Long-Term Goal

Transform the current Document Intelligence Engine into a scalable AI platform capable of enterprise document understanding, multi-document reasoning, autonomous research assistance, and production-grade document intelligence services.
