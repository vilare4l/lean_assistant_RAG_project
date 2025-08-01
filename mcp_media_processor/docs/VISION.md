# Vision du MCP Media Processor

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_media_processor` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_media_processor` est responsable de l'ingestion et du traitement de divers formats de médias (images, audio, vidéo) afin d'en extraire du contenu textuel et de le transformer en un `MCPPayload` standardisé. Ce payload sera ensuite utilisé pour alimenter les bases de données vectorielles et le graphe de connaissances.

## 2. Fonctionnalités Clés

- Extraction de texte à partir d'images (OCR).
- Transcription de l'audio (Speech-to-Text).
- Description de contenu visuel via des modèles de vision (Image Captioning).
- Gestion des métadonnées associées à chaque média et à ses chunks.
- Support de formats de fichiers variés (JPG, PNG, MP3, WAV, etc.).
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_media_processor` est un service d'ingestion clé, recevant des requêtes des agents (notamment le `Deep Research Crew`) et produisant des `MCPPayload` pour le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Critères de Succès

- Haute précision de l'extraction de texte et de la transcription audio.
- Qualité pertinente des descriptions d'images.
- Robustesse face à une grande variété de médias.
- Performance d'ingestion acceptable pour des volumes importants.
- Facilité d'intégration et de maintenance.
