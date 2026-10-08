# Prior Authorization Appeal Builder

An AI-powered healthcare workflow designed to analyze prior authorization denials, evaluate patient documentation against payer requirements, and generate evidence-grounded appeal drafts.

The project is being developed into an end-to-end Applied AI system incorporating retrieval-augmented generation (RAG), agentic orchestration, structured validation, and deployment-oriented engineering.

**Status:** Active Development

## Overview

Prior authorization appeals often require reviewing denial letters, identifying payer-specific coverage criteria, locating supporting clinical evidence, and preparing a structured appeal.

This project explores how LLM-powered workflows can automate portions of that process while maintaining traceability between policy requirements, patient evidence, and generated claims.

The current implementation is a modular, multi-stage Python pipeline. Future development focuses on scalable policy retrieval, agentic reasoning, verification, evaluation, and deployment.

## Current Implementation

The following pipeline stages have been implemented:

1. **Denial Extraction:** Extracts structured information from denial documents, including payer, medication, denial reason, and relevant patient information.
2. **Structured Validation:** Validates extracted information using Pydantic schemas.
3. **Policy Lookup:** Identifies applicable payer requirements and individual authorization criteria from supported policy references.
4. **Evidence Extraction:** Extracts relevant supporting information from patient documentation and associates it with policy criteria.
5. **Sufficiency Evaluation:** Evaluates whether the available evidence satisfies each identified requirement.
6. **Appeal Generation:** Produces structured, patient-specific appeal drafts using extracted evidence and policy requirements.

### Current Workflow

    Denial Letter + Patient Documentation
                     |
                     v
             Denial Extraction
                     |
                     v
            Structured Validation
                     |
                     v
               Policy Lookup
                     |
                     v
             Evidence Extraction
                     |
                     v
            Sufficiency Evaluation
                     |
                     v
              Appeal Generation
                     |
                     v
                 Appeal Draft

The pipeline uses structured data models to pass information between stages, separating extraction, policy interpretation, evidence assessment, and generation.

## Technology Stack

### Currently Implemented

- Python 3.12
- Anthropic API
- Pydantic
- Structured LLM outputs
- Prompt-based extraction and reasoning
- python-dotenv
- Standard Python utilities for file handling and data processing

### Planned Integrations

- LangChain
- LangGraph
- Retrieval-Augmented Generation (RAG)
- Embedding models and vector databases
- Docker
- REST API
- Automated testing and evaluation
- CI/CD and cloud deployment

Planned technologies are not represented as completed integrations.

## Planned System Architecture

The next development phase will extend the current sequential pipeline into a retrieval-grounded, stateful agentic workflow.

    Denial + Clinical Documentation
                  |
                  v
          Document Processing
                  |
                  v
         Policy Knowledge Base
                  |
                  v
          Embedding + Indexing
                  |
                  v
             RAG Retrieval
                  |
                  v
         LangChain Components
                  |
                  v
        LangGraph Orchestration
                  |
           +------+------+
           |             |
           v             v
       Retrieval     Evaluation
           |             |
           +------+------+
                  |
                  v
           Appeal Generation
                  |
                  v
              Verification
                  |
                  v
          Acceptance Criteria
             /          \
        Not Met          Met
           |              |
           v              v
      Retry / Revise   Final Draft

This architecture is a development target, not the current deployed system.

## Development Roadmap

### Phase 1: Core LLM Pipeline

**Status: Implemented**

- Structured denial extraction
- Pydantic-based validation
- Payer policy criteria lookup
- Clinical evidence extraction
- Criterion-level sufficiency evaluation
- Structured appeal generation

### Phase 2: Retrieval-Augmented Generation

**Status: Planned**

Introduce a retrieval pipeline to support a larger and more maintainable collection of payer policies.

Planned functionality:

- Ingest and preprocess payer policy documents.
- Chunk documents while preserving policy sections and references.
- Generate embeddings for semantic retrieval.
- Store indexed policy chunks in a vector database.
- Retrieve relevant policy criteria based on denial context.
- Preserve source metadata for document-level citations.
- Evaluate retrieval relevance and evidence grounding.

The goal is to replace the limitations of static policy lookup with scalable, source-grounded retrieval.

### Phase 3: LangChain Integration

**Status: Planned**

Use LangChain to modularize retrieval, model interaction, prompting, and structured output handling.

Planned components:

- Reusable prompt templates
- Structured output parsers
- Retriever interfaces
- Model integration
- Retrieval and generation components

LangChain will support individual workflow components rather than replacing the existing business logic unnecessarily.

### Phase 4: LangGraph Agentic Orchestration

**Status: Planned**

Introduce LangGraph to coordinate the workflow using explicit state management and conditional transitions.

The planned graph will support:

- Persistent workflow state during execution
- Conditional routing based on evidence sufficiency
- Additional retrieval when evidence is insufficient
- Appeal revision following verification failures
- Bounded retry loops
- Explicit stopping conditions
- Failure handling and human-review escalation

The objective is to move from a fixed sequential pipeline toward an agentic workflow capable of evaluating its intermediate results before proceeding.

### Phase 5: Verification and Evaluation

**Status: Planned**

Implement a verification layer that checks whether generated appeals are supported by available evidence and applicable policy requirements.

Evaluation priorities:

- Denial extraction accuracy
- Policy retrieval relevance
- Evidence-to-criterion alignment
- Sufficiency judgment consistency
- Citation correctness
- Unsupported claim detection
- Appeal completeness
- End-to-end workflow reliability

Acceptance criteria will determine whether the system returns a draft, retries an intermediate stage, or flags the case for human review.

### Phase 6: Containerization and Deployment

**Status: Planned**

Package the application into a reproducible, testable environment.

Planned engineering work:

- Docker containerization
- Dependency and environment management
- REST API for submitting cases and retrieving results
- Automated unit and integration tests
- Structured logging and error handling
- CI/CD workflows
- Cloud deployment
- Configuration and secret management

Docker will provide a consistent execution environment across local development, testing, and deployment.

Any future handling of real patient information will require appropriate privacy, security, access-control, and regulatory safeguards.

## Long-Term Goal

Build an end-to-end healthcare AI prototype that can transform prior authorization denial documents into evidence-grounded, traceable appeal drafts.

The intended workflow is:

    Denial
       |
       v
    Policy Retrieval
       |
       v
    Criteria Identification
       |
       v
    Clinical Evidence Extraction
       |
       v
    Sufficiency Evaluation
       |
       v
    Appeal Generation
       |
       v
    Evidence Verification
       |
       v
    Final Appeal Draft

The emphasis is on modular AI engineering, retrieval quality, controlled agentic reasoning, reliable structured outputs, and measurable system performance.

## Limitations

- The current policy lookup implementation is not yet a full RAG system.
- LangChain and LangGraph integrations are planned.
- Automated verification and systematic end-to-end evaluation are not yet complete.
- Containerization and deployment infrastructure are planned.
- Generated appeals require human review before use.

This is an educational and applied AI engineering prototype. It is not a clinically validated system and should not be used for autonomous medical, insurance, or coverage decisions.

## Author

Samer Ahmed

MS Artificial Intelligence, Northeastern University
