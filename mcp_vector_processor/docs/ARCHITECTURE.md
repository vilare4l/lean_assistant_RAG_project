# Architecture du MCP Vector Processor

Ce document détaille l'architecture technique du microservice `mcp_vector_processor`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (pour la réception des streams SSE)
- **Librairies de Traitement** : `openai` (pour la génération d'embeddings), `sqlalchemy` (pour l'interaction avec PostgreSQL/Supabase).
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint de réception SSE** : Reçoit les `MCPPayload` des MCPs d'ingestion.
- **Module `processor.py`** : Orchestre le processus de génération d'embeddings et de stockage.
- **Module `llm_client.py`** : Gère les appels aux modèles d'embedding (ex: OpenAI).
- **Module `db_client.py`** : Contient la logique d'interaction avec la base de données Supabase (insertion, mise à jour, suppression de vecteurs).
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py`.

## 3. Flux de Données

1. Les MCPs d'ingestion streament des `MCPPayload` vers le `mcp_vector_processor`.
2. Le `mcp_vector_processor` extrait le `content` de chaque `Chunk`.
3. Le `content` est envoyé à un modèle d'embedding (via `llm_client.py`) pour générer son vecteur.
4. Le vecteur, le `content` original et les `metadata` sont stockés dans la table `documents` de Supabase (via `db_client.py`).

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des `MCPPayload`.
- Optimisation des appels aux modèles d'embedding pour minimiser la latence et les coûts.
- Gestion des transactions de base de données pour des écritures performantes.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
