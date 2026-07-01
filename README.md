Part 1
---------
Project Banner
Overview
Problem Statement
Vision
Features
Tech Stack

Part 2
---------
Architecture
Folder Structure
Installation
Running Pipeline

Part 3
---------
GraphRAG Workflow
Report Generation
Current Capabilities
Example Outputs

Part 4
---------
Roadmap
Future Improvements
Contributing
License
Acknowledgements

# 🚀 Document Intelligence Engine

> **An AI-powered Document Intelligence Platform that combines Retrieval-Augmented Generation (RAG), GraphRAG, Knowledge Graphs, Hybrid Retrieval, and Large Language Models to understand, reason over, and generate insights from technical documents.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![GraphRAG](https://img.shields.io/badge/GraphRAG-Knowledge%20Graphs-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![LLM](https://img.shields.io/badge/LLM-GPT--4o--mini-red)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)

</p>

---

# 📖 Overview

Document Intelligence Engine is a modular AI framework designed to transform unstructured PDF documents into structured, searchable, and explainable knowledge.

Unlike traditional Retrieval-Augmented Generation (RAG) systems that rely only on semantic similarity, this project integrates a Knowledge Graph and GraphRAG pipeline to enhance contextual understanding, relationship reasoning, and factual grounding.

The system extracts entities, relationships, concepts, and semantic information from technical documents, builds a knowledge graph, performs hybrid retrieval using both vector search and graph traversal, and generates structured outputs such as technical reports, executive summaries, and question-answering responses.

The architecture has been designed to be modular, making it easy to extend with additional document intelligence capabilities such as multi-document reasoning, citation generation, table understanding, timeline extraction, and autonomous AI research assistants.

---

# ❓ Problem Statement

Traditional document question-answering systems suffer from several limitations:

* Semantic search often retrieves relevant text but fails to understand relationships between concepts.
* Information remains fragmented across document chunks.
* Complex technical questions require reasoning over multiple entities rather than isolated passages.
* Most RAG systems lack explainability and structured knowledge representation.
* Generating high-quality summaries and reports from long technical documents remains challenging.

This project addresses these challenges by combining semantic retrieval with graph-based reasoning to create a richer and more reliable document intelligence pipeline.

---

# 🎯 Vision

The long-term vision of this project is to build a complete AI-powered Document Intelligence Platform capable of:

* Reading and understanding technical documents.
* Building structured knowledge from unstructured text.
* Performing GraphRAG-based reasoning.
* Answering complex technical questions.
* Generating executive summaries and technical reports.
* Supporting cross-document reasoning.
* Assisting researchers, engineers, and organizations with intelligent document analysis.

Ultimately, the platform aims to evolve into an AI Research Assistant capable of understanding large collections of documents rather than individual PDFs.

---

# ✨ Current Features

## 📄 Document Processing

* PDF Extraction
* Text Normalization
* Metadata Extraction
* Semantic Chunking

## 🧠 Knowledge Extraction

* Entity Extraction
* Relationship Extraction
* Concept Extraction
* Knowledge Graph Generation
* Entity Alias Support
* Graph Cleaning Pipeline

## 🔍 Retrieval

* Sentence Transformer Embeddings
* ChromaDB Vector Search
* Semantic Retrieval
* Multi-Entity Detection
* Graph Expansion
* Graph Retrieval
* Hybrid Retrieval Ranking
* Context Fusion

## 🤖 AI Reasoning

* Retrieval-Augmented Generation (RAG)
* GraphRAG
* GPT-4o-mini Integration
* Prompt Engineering
* Context Builder

## 📑 Document Intelligence

* Executive Summary Generation
* Technical Report Generation
* Structured Report Generation
* Intelligent Question Answering

## 📤 Export

* DOCX Export
* PDF Export

---

# 🛠️ Technology Stack

| Category             | Technologies                             |
| -------------------- | ---------------------------------------- |
| Programming Language | Python 3.12                              |
| LLM                  | GPT-4o-mini (OpenRouter)                 |
| Embeddings           | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database      | ChromaDB                                 |
| Framework            | LangChain                                |
| Knowledge Graph      | Custom Graph Pipeline                    |
| Document Parsing     | PyMuPDF                                  |
| PDF Export           | ReportLab                                |
| DOCX Export          | python-docx                              |
| Visualization        | Vis Network                              |
| Development          | VS Code                                  |

---
# 🏗️ System Architecture

The Document Intelligence Engine follows a modular pipeline where each stage has a clearly defined responsibility.

```text
                    PDF Document
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
            Embedding Generation Layer
                          │
                          ▼
              ChromaDB Vector Database
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
 Knowledge Extraction              Semantic Retrieval
        │                                   │
        ▼                                   │
 Knowledge Graph                            │
        │                                   │
        ▼                                   ▼
    Graph Retrieval                 Retrieved Chunks
        └─────────────────┬─────────────────┘
                          ▼
                   Hybrid Ranking
                          │
                          ▼
                    Context Builder
                          │
                          ▼
                  GPT-4o-mini (LLM)
                          │
                          ▼
             Document Intelligence Layer
        ┌─────────────┬──────────────┬──────────────┐
        ▼             ▼              ▼              ▼
   Question       Executive     Technical      Structured
   Answering      Summary         Report          Report
                          │
                          ▼
                   Export Pipeline
                  DOCX / PDF Output
```

---

# 📂 Repository Structure

```text
Document-Intelligence-Engine/

├── app/
│
│   ├── extraction/
│   ├── normalization/
│   ├── embeddings/
│   ├── retrieval/
│   ├── reasoning/
│   ├── intelligence/
│   ├── exporters/
│   ├── visualization/
│   ├── knowledge_extraction/
│   └── classification/
│
├── data/
│   ├── extracted/
│   ├── normalized/
│   ├── knowledge/
│   └── vectors/
│
├── schemas/
│
├── tests/
│
├── docs/
│
├── README.md
├── CLAUDE.md
├── PROJECT_STATUS.md
├── ARCHITECTURE.md
├── DEVELOPMENT_GUIDE.md
└── ROADMAP.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Amrit14feb/document-intelligence-engine.git

cd document-intelligence-engine
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Create a `.env` file.

```env
OPENROUTER_API_KEY=YOUR_KEY
```

---

## Download Embedding Model

The project uses

```
all-MiniLM-L6-v2
```

which downloads automatically on first execution.

---

# 🚀 Running the Complete Pipeline

## Step 1

Extract PDF

```bash
python -m tests.test_pdf_parser
```

---

## Step 2

Normalize Document

```bash
python -m tests.test_normalization
```

---

## Step 3

Chunk Document

```bash
python -m tests.test_chunking
```

---

## Step 4

Generate Embeddings

```bash
python -m tests.test_embeddings
```

---

## Step 5

Build Knowledge Graph

```bash
python -m tests.test_graph
```

---

## Step 6

Run GraphRAG

```bash
python -m app.reasoning.rag_engine
```

---

## Step 7

Generate Executive Summary

```bash
python -m tests.test_summary
```

---

## Step 8

Generate Technical Report

```bash
python -m tests.test_structured_report
```

---

## Step 9

Export DOCX

```bash
python -m tests.test_docx_export
```

---

## Step 10

Export PDF

```bash
python -m tests.test_pdf_export
```

---

# 📦 Output Artifacts

The pipeline generates:

```text
data/

extracted/

normalized/

knowledge/

vectors/

outputs/

technical_report.docx

technical_report.pdf

summary.pdf

summary.docx
```

---
# 🧠 GraphRAG Workflow

Unlike traditional RAG systems that rely solely on semantic similarity, this project combines vector retrieval with graph-based reasoning to provide richer, more explainable responses.

## Workflow

```text
User Question
      │
      ▼
Entity Detection
      │
      ▼
Multi-Entity Detection
      │
      ▼
Graph Expansion
      │
      ▼
Knowledge Graph Retrieval
      │
      ├──────────────┐
      ▼              │
Semantic Retrieval   │
      │              │
      └──────┬───────┘
             ▼
      Hybrid Ranking
             ▼
      Context Builder
             ▼
       GPT-4o-mini
             ▼
 Generated Response
```

---

# 🕸️ Knowledge Graph Pipeline

The Knowledge Graph is constructed during document processing.

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Entity Extraction
 │
 ▼
Relationship Extraction
 │
 ▼
Concept Extraction
 │
 ▼
Knowledge Graph Builder
 │
 ▼
knowledge_graph.json
```

The generated graph currently stores:

* Entities
* Relationships
* Concepts
* Entity aliases
* Cleaned relationships

These graph components are used during GraphRAG retrieval to enrich semantic search.

---

# 🔍 Hybrid Retrieval Strategy

The retrieval engine combines two independent retrieval mechanisms.

## 1. Semantic Retrieval

Uses Sentence Transformer embeddings and ChromaDB to retrieve semantically similar document chunks.

Input:

```text
User Question
```

Output:

```text
Top N Relevant Chunks
```

---

## 2. Graph Retrieval

Uses detected entities to search the Knowledge Graph.

Input:

```text
Detected Entities
```

Output:

```text
Related entities

Relationships

Connected concepts
```

---

## 3. Hybrid Ranking

Both retrieval outputs are merged and reranked.

The final context contains

* Graph Knowledge
* Semantic Knowledge

before being sent to the LLM.

---

# 🧩 Current Pipeline Modules

| Module                  | Status |
| ----------------------- | ------ |
| PDF Extraction          | ✅      |
| Text Normalization      | ✅      |
| Chunk Generation        | ✅      |
| Embedding Generation    | ✅      |
| ChromaDB Storage        | ✅      |
| Semantic Retrieval      | ✅      |
| Entity Extraction       | ✅      |
| Relationship Extraction | ✅      |
| Concept Extraction      | ✅      |
| Knowledge Graph         | ✅      |
| Graph Retrieval         | ✅      |
| Graph Expansion         | ✅      |
| Hybrid Ranking          | ✅      |
| Hybrid Fusion Scorer    | ✅      |
| Entity Resolution       | ✅      |
| Graph Traversal (BFS)   | ✅      |
| Citation Generation     | ✅      |
| Confidence Scoring      | ✅      |
| Multi-document Graph    | ✅ (foundation) |
| Context Builder         | ✅      |
| GPT Integration         | ✅      |
| Executive Summary       | ✅      |
| Technical Report        | ✅      |
| Structured Report       | ✅      |
| DOCX Export             | ✅      |
| PDF Export              | ✅      |

---

# 📊 Current Capabilities

The engine can currently:

* Process PDF documents.
* Build normalized document representations.
* Generate semantic chunks.
* Generate sentence embeddings.
* Store vectors in ChromaDB.
* Retrieve relevant document chunks.
* Extract entities and relationships.
* Build a searchable knowledge graph.
* Perform GraphRAG-based retrieval.
* Fuse graph and semantic context.
* Answer technical questions.
* Generate executive summaries.
* Generate structured technical reports.
* Export reports to DOCX and PDF.

---

# 📷 Example Outputs

## Question Answering

```text
Question

What is the objective of the SAToC architecture?

↓

GraphRAG Retrieval

↓

Hybrid Context

↓

GPT Response
```

---

## Executive Summary

```text
PDF

↓

Summary Generator

↓

Executive Summary
```

---

## Technical Report

```text
PDF

↓

Structured Report Generator

↓

DOCX

↓

PDF
```

---

## Knowledge Graph

```text
Entity

↓

Relationship

↓

Connected Entity

↓

Graph Traversal

↓

Reasoning
```

---

# 🎯 Design Principles

The project follows several architectural principles:

* Modular architecture
* Independent pipeline stages
* Easy extensibility
* Separation of concerns
* Explainable retrieval
* Reusable components
* Minimal coupling
* Future-ready GraphRAG design

These principles allow new modules such as citation generation, timeline extraction, table understanding, and diagram analysis to be added without major architectural changes.

---
# 🗺️ Project Roadmap

The project is being developed incrementally toward a complete AI-powered Document Intelligence Platform.

## Version 1.0 (Completed)

* ✅ PDF Extraction
* ✅ Text Normalization
* ✅ Semantic Chunking
* ✅ Sentence Embeddings
* ✅ ChromaDB Integration
* ✅ Semantic Retrieval
* ✅ Entity Extraction
* ✅ Relationship Extraction
* ✅ Concept Extraction
* ✅ Knowledge Graph Construction
* ✅ GraphRAG Integration
* ✅ Hybrid Retrieval
* ✅ Executive Summary Generation
* ✅ Technical Report Generation
* ✅ Structured Report Generation
* ✅ DOCX Export
* ✅ PDF Export

---

## Version 1.5 (In Progress)

* 🔄 Improved Retrieval Quality
* 🔄 Better Hybrid Ranking
* 🔄 Enhanced Graph Traversal
* 🔄 Better Entity Linking
* 🔄 Prompt Optimization
* 🔄 Improved Report Quality

---

## Version 2.0 (Planned)

* Citation Generation
* Source Referencing
* Confidence Scores
* Timeline Extraction
* Table Extraction
* Figure Extraction
* OCR Support
* Metadata Enrichment

---

## Version 3.0 (Future)

* Multi-document GraphRAG
* Cross-document Reasoning
* Research Paper Comparison
* Automatic Literature Review
* Interactive Knowledge Graph
* REST API
* Web Dashboard

---

## Version 4.0 (Long-Term Vision)

* Autonomous AI Research Assistant
* Multi-Agent Reasoning
* Continuous Knowledge Base Updates
* Enterprise Document Intelligence
* Cloud Deployment
* Collaboration Features

---

# 🤝 Contributing

Contributions are welcome.

If you plan to extend the project:

* Keep the architecture modular.
* Avoid tightly coupling new modules.
* Prefer extending existing components rather than rewriting them.
* Maintain compatibility with the GraphRAG pipeline.
* Add tests for new functionality.
* Update documentation when introducing new modules.

---

# 📌 Current Development Focus

The current development effort is focused on improving the quality of retrieval and reasoning.

Primary goals include:

* Increasing retrieval precision.
* Improving graph traversal.
* Enhancing entity disambiguation.
* Generating richer technical reports.
* Supporting multi-document intelligence.

---

# 📚 Repository Documentation

Additional documentation is available in the repository.

| File                 | Description                                              |
| -------------------- | -------------------------------------------------------- |
| README.md            | Project overview                                         |
| CLAUDE.md            | Instructions for Claude Code and AI-assisted development |
| PROJECT_STATUS.md    | Current implementation status                            |
| ARCHITECTURE.md      | Detailed system architecture                             |
| DEVELOPMENT_GUIDE.md | Developer onboarding guide                               |
| ROADMAP.md           | Planned features and milestones                          |
| CONTRIBUTING.md      | Contribution guidelines                                  |
| CHANGELOG.md         | Project history                                          |

---

# 🙏 Acknowledgements

This project builds upon ideas and technologies from the following communities:

* LangChain
* ChromaDB
* Sentence Transformers
* Hugging Face
* OpenRouter
* ReportLab
* python-docx

Special thanks to the open-source AI community for providing the tools and libraries that make projects like this possible.

---

# 📄 License

This project is released for educational and research purposes.

Future licensing may be updated as the project evolves.

---

<p align="center">

**⭐ If you find this project useful, consider starring the repository and following its development.**

</p>
