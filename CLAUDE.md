# CLAUDE.md

# Document Intelligence Engine

## Project Purpose

Document Intelligence Engine is an AI-powered platform for understanding technical documents using Retrieval-Augmented Generation (RAG), Knowledge Graphs, and GraphRAG.

The long-term objective is to evolve the project into a complete AI Research Assistant capable of understanding multiple technical documents, reasoning over them, and generating high-quality reports.

---

# Development Philosophy

This project is designed around modularity.

Every component should have a single responsibility.

Avoid tightly coupling modules.

New functionality should be implemented as new modules rather than modifying unrelated existing code.

---

# Current Architecture

PDF

↓

Extraction

↓

Normalization

↓

Chunking

↓

Embeddings

↓

ChromaDB

↓

Knowledge Extraction

├── Entity Extraction

├── Relationship Extraction

└── Concept Extraction

↓

Knowledge Graph

↓

Graph Retrieval

*

Semantic Retrieval

↓

Hybrid Ranking

↓

Context Builder

↓

GPT-4o-mini

↓

Document Intelligence

↓

DOCX / PDF Export

---

# Completed Modules

## Extraction

* PDF Parsing
* Structured JSON Generation

---

## Normalization

* Text Cleaning
* Metadata Extraction

---

## Chunking

* Semantic Chunk Generation

---

## Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

---

## Vector Database

* ChromaDB

---

## Retrieval

* Semantic Retrieval
* Multi Entity Detection
* Graph Retrieval
* Graph Expansion
* Hybrid Ranking

---

## Knowledge Extraction

* Entity Extraction
* Relationship Extraction
* Concept Extraction
* Knowledge Graph Generation

---

## Reasoning

* GraphRAG
* Context Builder
* GPT Integration

---

## Intelligence

* Executive Summary
* Technical Report
* Structured Report

---

## Export

* DOCX
* PDF

---

# Current Folder Responsibilities

app/

Contains all source code.

data/

Contains generated artifacts.

Do not hardcode data paths.

schemas/

Contains document schemas.

tests/

Contains independent module testing.

lib/

Visualization libraries.

---

# Current Retrieval Pipeline

User Question

↓

Entity Detection

↓

Graph Expansion

↓

Semantic Retrieval

↓

Graph Retrieval

↓

Hybrid Ranking

↓

Context Builder

↓

LLM

↓

Answer

---

# Coding Rules

Always follow these rules.

1.

Keep every module independent.

2.

Never mix retrieval logic with report generation.

3.

Never mix graph logic with semantic retrieval.

4.

Keep prompts inside

app/reasoning/prompts.py

5.

Avoid duplicated code.

6.

Prefer reusable functions.

7.

Every new feature should be testable independently.

8.

Do not break existing GraphRAG functionality.

---

# Existing Technologies

Python

LangChain

Sentence Transformers

ChromaDB

OpenRouter

GPT-4o-mini

ReportLab

python-docx

PyMuPDF

---

# Current Known Limitations

Retrieval quality can still be improved.

Relationship extraction needs better filtering.

Entity linking needs improvement.

No citation generation.

No multi-document support.

No table understanding.

No diagram understanding.

---

# High Priority Future Work

Improve Hybrid Ranking.

Improve Graph Traversal.

Improve Entity Resolution.

Add Citation Generation.

Add Confidence Scores.

Improve Report Generation.

Improve Summary Quality.

---

# Planned Features

Multi-document RAG

Multi-document GraphRAG

Timeline Extraction

Table Extraction

Diagram Extraction

Figure Caption Understanding

Source Citation

Interactive Knowledge Graph

REST API

Web Interface

Research Assistant

---

# Never Break

The following modules are considered stable.

Semantic Retrieval

Knowledge Graph

Graph Expansion

Context Builder

Summary Generation

Report Generation

DOCX Export

PDF Export

---

# Preferred Coding Style

Small functions.

Descriptive variable names.

No duplicated logic.

Type hints when possible.

Docstrings for public functions.

Readable code over clever code.

---

# Testing

Every new feature must include an independent test inside

tests/

Never merge untested code.

---

# Goal

Transform this repository into a production-ready Document Intelligence Platform capable of understanding, reasoning over, and generating knowledge from complex technical documents.
