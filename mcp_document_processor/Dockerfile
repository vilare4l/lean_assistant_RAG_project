FROM python:3.12-slim

ARG PORT=8050

WORKDIR /app

# Install system dependencies for unstructured (PDF, DOCX)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libxml2-dev \
    libxslt1-dev \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    antiword \
    unzip \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# Install uv (or pip if you prefer)
RUN pip install uv

# Copy the MCP server files
COPY . .

# Install packages
RUN python -m venv .venv
RUN uv pip install -e .

EXPOSE ${PORT}

# Command to run the MCP server
CMD ["uv", "run", "src/main.py"]

