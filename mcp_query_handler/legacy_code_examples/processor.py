# core/mcp-servers/query-handler/processor.py
from . import db_clients, llm_client
from .main import QueryRequest

async def process_query(request: QueryRequest) -> tuple[str, list]:
    """Route la requête et orchestre la génération de la réponse."""
    
    context_data = []
    
    if request.query.startswith("/graph"):
        # Branche Neo4j
        graph_query = request.query.replace("/graph", "").strip()
        # Pour le MVP, on peut imaginer une traduction simple ou un LLM pour générer le Cypher
        # NOTE: This is a simplified query for demonstration purposes.
        cypher = f"MATCH (c) WHERE c.name CONTAINS '{graph_query}' RETURN c.name as name, c.file_path as path LIMIT 10"
        raw_context = await db_clients.neo4j_execute(cypher)
        context_text = f"Résultats du graphe : {raw_context}"
        context_data = raw_context
    else:
        # Branche sémantique (défaut)
        query_embedding = await llm_client.get_embedding(request.query)
        raw_context = await db_clients.postgres_execute_match(
            embedding=query_embedding,
            source_filter=request.source_id,
            type_filter=request.chunk_type
        )
        context_text = "\n---\n".join([item['content'] for item in raw_context])
        context_data = raw_context

    # Génération de la réponse finale avec le LLM
    final_answer = await llm_client.get_completion(request.query, context_text)
    
    return final_answer, context_data

