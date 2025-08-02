# Vision du MCP Document Processor

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_document_processor` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_document_processor` est responsable de l'ingestion et du traitement de divers formats de documents (PDF, DOCX, CSV, XLSX, etc.) afin de les transformer en un `MCPPayload` standardisé et enrichi. Ce payload sera ensuite utilisé pour alimenter les bases de données vectorielles et le graphe de connaissances.

## 2. Fonctionnalités Clés

- Extraction de texte à partir de documents structurés et non structurés.
- Identification et extraction de données tabulaires (tableaux) avec conservation de leur structure.
- **Détection et référencement des images et schémas intégrés dans les documents pour un traitement ultérieur par le `mcp_media_processor`.**
- Gestion des métadonnées associées à chaque document et à ses chunks.
- Support de formats de fichiers variés.
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_document_processor` est un service d'ingestion clé, recevant des requêtes des agents (notamment le `Deep Research Crew`) et produisant des `MCPPayload` pour le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Critères de Succès

- Haute précision de l'extraction de texte et de données tabulaires.
- Robustesse face à une grande variété de documents et de structures.
- Performance d'ingestion acceptable pour des volumes importants.
- Facilité d'intégration et de maintenance.
