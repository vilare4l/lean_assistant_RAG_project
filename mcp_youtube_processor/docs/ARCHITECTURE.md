# Architecture du MCP YouTube Processor

Ce document détaille l'architecture technique du microservice `mcp_youtube_processor`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (avec support SSE pour le streaming des résultats)
- **Librairies de Traitement** : `youtube-transcript-api` pour la récupération des transcriptions.
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint `/process-youtube/`** : Reçoit les URLs YouTube à traiter.
- **Module `processor.py`** : Contient la logique d'extraction de l'ID vidéo, la récupération de la transcription et le chunking.
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py` pour la structure des données entrantes et sortantes.

## 3. Flux de Données

1. Un agent (ex: `Deep Research Crew`) envoie une URL YouTube au `mcp_youtube_processor` via l'endpoint `/process-youtube/`.
2. Le `mcp_youtube_processor` extrait l'ID vidéo et utilise `youtube-transcript-api` pour récupérer la transcription.
3. La transcription est chunkée (par exemple, par groupes de segments) et les métadonnées sont ajoutées.
4. Un `MCPPayload` est construit avec les informations de la source et les chunks de transcription.
5. Le `MCPPayload` est streamé (via SSE) vers le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Considérations de Performance et Scalabilité

- Traitement synchrone ou asynchrone des requêtes (dépend de la librairie `youtube-transcript-api`).
- Gestion des erreurs pour les vidéos sans transcription ou les URLs invalides.
- Optimisation du chunking pour la recherche sémantique.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
