// shared/database_schemas/neo4j_schema.cypher

// Basic Node Labels and Relationship Types for an enriched Knowledge Graph
// This schema is a starting point and will evolve as entity extraction logic matures.

// 1. Source Node: Represents the origin of the information (e.g., a document, a web page, a YouTube video)
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Source) REQUIRE s.id IS UNIQUE;
// Properties: id (from MCPPayload.source_info.source_id), type (e.g., 'web_page', 'pdf_document', 'youtube_video'), summary, url, etc.

// 2. Chunk Node: Represents a processed piece of content from a Source
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE;
// Properties: id (UUID), content_preview (short snippet), type (e.g., 'text', 'code', 'table'), metadata (JSONB of original chunk metadata)

// 3. Entity Node: Represents any named entity extracted from content (e.g., Person, Organization, Concept, Technology, Location)
CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;
// Properties: name, type (e.g., 'Person', 'Organization', 'Product', 'Concept'), description, etc.

// 4. Relationship Types (Examples):

// (Source)-[:CONTAINS_CHUNK]->(Chunk)
// (Chunk)-[:MENTIONS]->(Entity)
// (Entity)-[:RELATED_TO]->(Entity)
// (Person)-[:WORKS_AT]->(Organization)
// (Concept)-[:DEFINED_IN]->(Source)
// (Product)-[:USED_IN]->(Project)

// Example of creating a Source and linking a Chunk and an Entity:
// MERGE (s:Source {id: 'doc_123', type: 'pdf_document', summary: 'Summary of doc 123'})
// MERGE (c:Chunk {id: 'chunk_abc', content_preview: '...', type: 'text'})
// MERGE (e:Entity {name: 'Lean Manufacturing', type: 'Concept'})
// MERGE (s)-[:CONTAINS_CHUNK]->(c)
// MERGE (c)-[:MENTIONS]->(e)

// Example of a more specific relationship:
// MERGE (p:Person {name: 'Taiichi Ohno'})
// MERGE (c:Concept {name: 'Toyota Production System'})
// MERGE (p)-[:DEVELOPED]->(c)

// Note: The mcp_graph_enricher will be responsible for dynamically creating these nodes and relationships
// based on LLM extraction from MCPPayloads.
