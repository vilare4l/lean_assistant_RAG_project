# Vision du MCP YouTube Processor

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_youtube_processor` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_youtube_processor` est responsable de l'ingestion de contenu à partir d'URLs YouTube, en extrayant les transcriptions des vidéos et en les transformant en un `MCPPayload` standardisé. Ce payload sera ensuite utilisé pour alimenter les bases de données vectorielles et le graphe de connaissances.

## 2. Fonctionnalités Clés

- Extraction des identifiants de vidéo à partir d'URLs YouTube.
- Récupération des transcriptions de vidéos YouTube (si disponibles).
- Chunking des transcriptions pour optimiser la pertinence des embeddings.
- Gestion des métadonnées (ID vidéo, URL, timestamps) associées aux transcriptions.
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_youtube_processor` est un service d'ingestion clé, recevant des requêtes des agents (notamment le `Deep Research Crew`) et produisant des `MCPPayload` pour le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Critères de Succès

- Capacité à récupérer les transcriptions pour une large gamme de vidéos YouTube.
- Robustesse face aux URLs invalides ou aux vidéos sans transcription.
- Performance d'ingestion acceptable.
- Qualité des chunks générés pour la recherche sémantique.
- Facilité d'intégration et de maintenance.
