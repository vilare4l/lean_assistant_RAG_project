# Vision du MCP Web Crawler

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_web_crawler` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_web_crawler` est responsable de l'ingestion de contenu à partir d'URLs web, en extrayant le texte, les blocs de code et les métadonnées pertinentes, afin de les transformer en un `MCPPayload` standardisé. Ce payload sera ensuite utilisé pour alimenter les bases de données vectorielles et le graphe de connaissances.

## 2. Fonctionnalités Clés

- Crawling de pages web et extraction de leur contenu principal.
- Conversion du contenu HTML en Markdown pour une meilleure structuration.
- Chunking intelligent du contenu pour optimiser la pertinence des embeddings.
- Extraction des blocs de code et génération de résumés pour ces blocs.
- Gestion des métadonnées (URL, titres, etc.) associées au contenu web.
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_web_crawler` est un service d'ingestion clé, recevant des requêtes des agents (notamment le `Deep Research Crew`) et produisant des `MCPPayload` pour le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Critères de Succès

- Haute précision de l'extraction de contenu web pertinent.
- Robustesse face à la diversité des structures de pages web.
- Performance de crawling acceptable.
- Qualité des chunks générés pour la recherche sémantique.
- Facilité d'intégration et de maintenance.
