-- shared/database_schemas/postgresql_schema.sql

-- Enable the pgvector extension for vector embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Table to store content chunks and their embeddings
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(255) NOT NULL, -- From SourceInfo.source_id
    chunk_type VARCHAR(50) NOT NULL, -- From Chunk.chunk_type (e.g., 'text', 'code', 'summary')
    content TEXT NOT NULL,            -- From Chunk.content
    metadata JSONB DEFAULT '{}',     -- From Chunk.metadata
    embedding VECTOR(1536),           -- OpenAI text-embedding-3-small dimension
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for efficient vector similarity search
-- (Requires building an HNSW or IVFFlat index for large datasets)
-- Example for HNSW (requires pgvector 0.5.0+):
-- CREATE INDEX ON documents USING hnsw (embedding vector_l2_ops);

-- Table to store tabular data
CREATE TABLE IF NOT EXISTS tabular_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(255) NOT NULL, -- Link to the original source
    table_name VARCHAR(255) NOT NULL, -- From TabularData.table_name
    row_data JSONB NOT NULL,         -- From TabularData.rows (each row as a JSON object)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table to store references to extracted media (images, diagrams, etc.)
CREATE TABLE IF NOT EXISTS extracted_media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(255) NOT NULL, -- Link to the original document source
    media_id VARCHAR(255) NOT NULL,  -- Unique identifier for the extracted media
    media_type VARCHAR(50) NOT NULL, -- Type of media (e.g., 'image', 'diagram', 'chart')
    file_path TEXT NOT NULL,         -- Path or URL to the stored media file
    metadata JSONB DEFAULT '{}',     -- Additional metadata (e.g., OCR text, description)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Index on source_id for faster lookup of all media from a specific source
CREATE INDEX IF NOT EXISTS idx_extracted_media_source_id ON extracted_media (source_id);

-- Optional: Index on source_id for faster lookup of all data from a specific source
CREATE INDEX IF NOT EXISTS idx_documents_source_id ON documents (source_id);
CREATE INDEX IF NOT EXISTS idx_tabular_data_source_id ON tabular_data (source_id);

-- Optional: Function for semantic search (similar to the one in legacy query-handler)
-- This function is typically used by the mcp_query_handler
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding VECTOR(1536),
    match_count INT DEFAULT NULL,
    source_filter VARCHAR(255) DEFAULT NULL,
    chunk_type_filter VARCHAR(50) DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    source_id VARCHAR(255),
    chunk_type VARCHAR(50),
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.source_id,
        d.chunk_type,
        d.content,
        d.metadata,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM
        documents d
    WHERE
        (source_filter IS NULL OR d.source_id = source_filter) AND
        (chunk_type_filter IS NULL OR d.chunk_type = chunk_type_filter)
    ORDER BY
        d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
