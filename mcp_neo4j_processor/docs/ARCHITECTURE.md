# Architecture du MCP Graph Enricher (anciennement Neo4j Processor)

Ce document détaille l'architecture technique du microservice `mcp_graph_enricher`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (pour la réception des streams SSE)
- **Librairies de Traitement** : `openai` (pour l'extraction d'entités/relations via LLM), `neo4j` (pour l'interaction avec la base de données graphe).
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint de réception SSE** : Reçoit les `MCPPayload` des MCPs d'ingestion.
- **Module `processor.py`** : Orchestre le processus d'extraction et de population du graphe.
- **Module `llm_client.py`** : Gère les appels aux LLMs pour l'extraction d'entités et de relations.
- **Module `graph_writer.py`** : Contient la logique de conversion des entités/relations en requêtes Cypher et d'interaction avec Neo4j.
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py`.

## 3. Flux de Données

1. Les MCPs d'ingestion streament des `MCPPayload` vers le `mcp_graph_enricher`.
2. Le `mcp_graph_enricher` extrait le `content` et les `metadata` de chaque `Chunk`.
3. Le `content` est envoyé à un LLM (via `llm_client.py`) avec un prompt spécifique pour l'extraction d'entités et de relations.
4. Les entités et relations extraites sont transformées en requêtes Cypher (via `graph_writer.py`).
5. Le graphe de connaissances dans Neo4j est mis à jour.

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des `MCPPayload`.
- Optimisation des prompts LLM pour une extraction efficace et économique.
- Gestion des transactions Neo4j pour des écritures performantes.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
