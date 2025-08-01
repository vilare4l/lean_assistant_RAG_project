# Architecture du MCP Query Handler

Ce document détaille l'architecture technique du microservice `mcp_query_handler`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI
- **Librairies de Traitement** : `openai` (pour la génération d'embeddings et la synthèse LLM), `sqlalchemy` (pour l'interaction avec PostgreSQL/Supabase), `neo4j` (pour l'interaction avec Neo4j).
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint `/query/`** : Reçoit les requêtes utilisateur.
- **Module `processor.py`** : Orchestre le processus de recherche et de synthèse.
- **Module `llm_client.py`** : Gère les appels aux LLMs pour la génération d'embeddings (pour la recherche sémantique) et la synthèse de réponses.
- **Module `db_clients.py`** : Contient la logique d'interaction avec Supabase (PostgreSQL) et Neo4j.
- **Modèles de Données** : Utilisation des schémas Pydantic pour les requêtes et réponses.

## 3. Flux de Données

1. Un agent utilisateur (ex: `Lean Assistant`) envoie une requête au `mcp_query_handler` via l'endpoint `/query/`.
2. Le `mcp_query_handler` (via `processor.py`) détermine la stratégie de recherche (sémantique, graphe, ou combinée).
3. Des appels sont faits à `db_clients.py` pour interroger Supabase (avec embeddings générés par `llm_client.py`) et/ou Neo4j.
4. Le contexte pertinent est récupéré des bases de données.
5. Le contexte et la requête originale sont envoyés à un LLM (via `llm_client.py`) pour la synthèse de la réponse.
6. La réponse synthétisée est retournée à l'agent utilisateur.

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des requêtes.
- Optimisation des requêtes de base de données pour minimiser la latence.
- Gestion des appels LLM pour la synthèse (coût et latence).
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
