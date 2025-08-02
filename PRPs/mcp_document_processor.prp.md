# PRP - MCP Document Processor

## 1. Goal

Implement the initial version of the `mcp_document_processor`, a FastAPI-based microservice that receives document files (PDF, DOCX, CSV), processes them, and outputs a standardized `MCPPayload`.

## 2. Why

This service is a core component of the ingestion pipeline. It's the first step to transform unstructured documents into a structured format that can be used by the `mcp_vector_processor` and `mcp_graph_enricher`.

## 3. What

- A FastAPI application.
- A single endpoint `/process-document/` that accepts file uploads.
- Logic to handle different MIME types (PDF, DOCX, CSV, XLSX).
- Use of the `unstructured` library for parsing PDF/DOCX and `pandas` for tabular data.
- The endpoint must return a valid `MCPPayload` object, including references to extracted images/diagrams.

### Success Criteria

- [ ] The service can be built into a Docker container.
- [ ] The service starts correctly with `uvicorn`.
- [ ] Sending a PDF file to `/process-document/` returns a valid `MCPPayload` with extracted text chunks.
- [ ] Sending a CSV file to `/process-document/` returns a valid `MCPPayload` with extracted tabular data.
- [ ] Sending a PDF/DOCX with embedded images/diagrams returns a `MCPPayload` with `extracted_media_references` populated.
- [ ] Sending a PDF with a clear table returns a `MCPPayload` with structured `tabular_data`.

## 4. All Needed Context

### Documentation & References

```yaml
# Core project documentation
- file: general/ARCHITECTURE.md
  why: Understand the global architecture and how this MCP fits in.

# Sub-project documentation
- file: mcp_document_processor/docs/VISION.md
  why: Specific vision for this microservice.
- file: mcp_document_processor/docs/ARCHITECTURE.md
  why: Specific architecture for this microservice.

# Shared schemas and database definitions
- file: shared/schemas/mcp_payload.py
  why: The data contract for the output of this service.
- file: shared/database_schemas/postgresql_schema.sql
  why: Understanding where the processed data will be stored.
- file: shared/database_schemas/neo4j_schema.cypher
  why: Understanding how extracted entities and media will be represented in the graph.

# Legacy code examples
- file: mcp_document_processor/src/main.py
  why: Example of FastAPI endpoint and structure.
- file: mcp_document_processor/src/parser.py
  why: Example of parsing logic using unstructured and pandas.
- file: mcp_document_processor/src/requirements.txt
  why: List of necessary Python dependencies.
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: The `unstructured` library can be slow and has many dependencies. Ensure the Docker build is efficient.
# CRITICAL: `pandas` can have issues with large Excel files. For now, we assume reasonable file sizes.
# CRITICAL: Ensure all file I/O is handled asynchronously to not block the FastAPI event loop.
# CRITICAL: Table extraction from PDFs can be challenging. `unstructured`'s `hi_res` strategy relies on Tesseract OCR, which needs to be installed and configured.
# CRITICAL: Image extraction from PDFs might require additional system dependencies or specific `unstructured` configurations.
```

## 5. Implementation Blueprint

### List of tasks to be completed

```yaml
Task 1: Setup FastAPI Application
  MODIFY mcp_document_processor/src/main.py:
    - Ensure the FastAPI app is correctly initialized.
    - Implement the `/process-document/` endpoint.
    - The endpoint should receive an `UploadFile`.

Task 2: Implement Parsing Logic
  MODIFY mcp_document_processor/src/parser.py:
    - Create a `parse_file` function that takes file content and MIME type.
    - Implement `_parse_unstructured_document` using `unstructured.partition`.
    - Implement `_parse_tabular_document` using `pandas`.
    - Ensure both functions return a valid `MCPPayload` object.
    - **Enhance PDF table extraction**: Investigate and implement methods to improve structured table extraction from PDFs (e.g., `unstructured` parameters, alternative libraries like `Camelot` or `Tabula-py`).
    - **Implement image/diagram extraction**: Extract embedded images/diagrams from PDFs and reference them in the `MCPPayload`.

Task 3: Integrate Parser with Endpoint
  MODIFY mcp_document_processor/src/main.py:
    - Call the `parse_file` function from the endpoint.
    - Return the resulting `MCPPayload`.

Task 4: Create Dockerfile
  MODIFY mcp_document_processor/src/Dockerfile:
    - Ensure it correctly copies the `src` directory.
    - Installs all dependencies from `requirements.txt`.
    - Exposes port 8000 and runs the application with `uvicorn`.
```

## 6. Validation Loop

### Level 1: Syntax & Style

```bash
# Ensure code is formatted correctly
black mcp_document_processor/src/

# Check for type errors
mypy mcp_document_processor/src/
```

### Level 2: Dependency Installation

```bash
# Install dependencies from requirements.txt
pip install -r mcp_document_processor/src/requirements.txt
```

### Level 3: Local Server Test

```bash
# Run the server locally
uvicorn mcp_document_processor.src.main:app --reload --port 8000

# In a separate terminal, send a test file:
# curl -X POST -F "file=@/path/to/your/test.pdf" http://localhost:8000/process-document/
```

### Level 4: Docker Build Test

```bash
# Build the Docker image
docker build -t mcp-document-processor -f mcp_document_processor/src/Dockerfile .

# Run the Docker container
docker run -p 8000:8000 mcp-document-processor
```
