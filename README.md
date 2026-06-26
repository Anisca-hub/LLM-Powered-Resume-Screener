🚀 LLM Powered Resume Screening Tool

A high-performance, LLM-driven ATS (Applicant Tracking System) emulator designed to bridge the semantic gap between candidate experience and job requirements. Built for precision, this engine moves beyond keyword matching by utilizing a hybrid orchestration pipeline that combines deterministic extraction with deep semantic understanding.


🔬 Engineering Philosophy

Traditional ATS systems rely on fragile, rule-based keyword matching. This engine leverages Retrieval-Augmented Generation (RAG) principles and Dense Vector Embeddings to ensure that "Machine Learning Engineer" matches "Data Scientist" based on conceptual proximity, not just string equality.


✨ Technical Architecture

1. Intelligent Parsing & Extraction

Resume Parser: Utilizes PyMuPDF for high-fidelity text extraction, feeding raw unstructured data into Gemini 2.5 Flash for hierarchical entity recognition.

JD Preprocessor: Implements deterministic noise removal and schema-strict extraction to ensure the LLM outputs valid, production-ready JSON.

Skill Normalization: Features a robust mapping layer that resolves synonyms and alias clusters (e.g., ML ↔ Machine Learning, NN ↔ Neural Networks) to a canonical ontology.

2. Hybrid Matching Engine

The core scoring logic aggregates intelligence from three distinct layers to provide a 360-degree candidate evaluation:

![System Architecture](matching-pipeline-architecture)


🏗️ Technical Stack

LLM Orchestration: google-genai SDK (Gemini 2.5 Flash)

Embedding Engine: sentence-transformers (all-MiniLM-L6-v2)

Backend: Modular Python (Core/Matching/Utils)

Parser: PyMuPDF

Data Integrity: json-repair for robust LLM output handling


🚀 Quick Start

Prerequisites

Python 3.10+

A valid Google AI Studio API Key


Installation

# Clone the repository

git clone https://github.com/Anisca-hub/LLM-Powered-Resume-Screener.git

cd "LLM Powered Resume Screener"

# Install dependencies

pip install -r requirements.txt


Configuration

Create a .env file in the root directory: GEMINI_API_KEY=your_key_here.

Place your resume in the root directory and rename it to sample_resume.pdf.

Place your target Job Description text into data/samples/sample_jd.txt.


Execution

Run the matching pipeline: python -m run_match


📊 Performance Insights

The engine produces a Transparent Scoring Report, enabling candidates and recruiters to see exactly why a match score was generated:

{

  "semantic_score": 0.919,

  "overall_score": 100,

  "strengths": [

    "Strong evidence for required skill: python",

    "Strong evidence for required skill: tensorflow",

    "Strong evidence for required skill: keras",

    "Projects align well with job responsibilities",

    "Skills are backed by concrete project or work evidence"

  ],

  "gaps": [],

  "suggestions": []

}


🛠️ Advanced Roadmap

Ontology Scaling: Transitioning to graph-based skill clustering.

Inference Optimization: Migrating from standard calls to batched embedding pipelines for faster processing.

UI Integration: Deployment via Streamlit for real-time candidate ranking.

Built by [Anisca Jha] | [https://www.linkedin.com/in/anisca-jha-93ba83308]