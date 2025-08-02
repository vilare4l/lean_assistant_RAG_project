# core/mcp-servers/query-handler/db_clients.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL (Supabase)
PG_DATABASE_URL = os.getenv("PG_DATABASE_URL")
if not PG_DATABASE_URL:
    raise ValueError("PG_DATABASE_URL environment variable not set.")

pg_engine = create_async_engine(PG_DATABASE_URL)
AsyncPGSessionLocal = sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)

# Neo4j
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    raise ValueError("Neo4j connection details not fully provided in environment variables.")

neo4j_driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

from sqlalchemy import text

async def postgres_execute_match(embedding: list[float], source_filter: str | None, type_filter: str, match_count: int = 10) -> list[dict]:
    """Exécute la fonction match_content_chunks dans PostgreSQL."""
    async with AsyncPGSessionLocal() as session:
        async with session.begin():
            stmt = text("""
                SELECT id, source_id, content, chunk_type, metadata, similarity
                FROM match_content_chunks(:query_embedding, :match_count, :source_filter, :type_filter)
            """)
            
            params = {
                "query_embedding": embedding,
                "match_count": match_count,
                "source_filter": source_filter,
                "type_filter": type_filter
            }
            
            result = await session.execute(stmt, params)
            rows = result.mappings().all()
            return [dict(row) for row in rows]

async def neo4j_execute(query: str) -> list[dict]:
    """Exécute une requête Cypher dans Neo4j."""
    async with neo4j_driver.session() as session:
        result = await session.run(query)
        records = await result.data()
        return records
