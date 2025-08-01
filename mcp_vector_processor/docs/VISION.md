# Vision du MCP Vector Processor

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_vector_processor` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_vector_processor` est responsable de la génération d'embeddings vectoriels à partir des `MCPPayload` reçus (provenant de toutes les sources d'ingestion) et de leur stockage dans la base de données vectorielle (Supabase/PostgreSQL avec pg_vector). Son but est de permettre la recherche sémantique et la récupération d'informations pertinentes.

## 2. Fonctionnalités Clés

- Réception des `MCPPayload` streamés depuis les MCPs d'ingestion.
- Utilisation de modèles d'embedding (OpenAI par défaut) pour convertir le contenu textuel des chunks en vecteurs numériques.
- Stockage des vecteurs et des métadonnées associées dans la base de données Supabase (table `documents`).
- Gestion des mises à jour et suppressions de documents dans la base vectorielle.
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_vector_processor` est un processeur de données central, recevant des `MCPPayload` de tous les MCPs d'ingestion et alimentant la base de données Supabase. Il travaille en parallèle avec le `mcp_graph_enricher`.

## 4. Critères de Succès

- Haute qualité des embeddings générés pour une recherche sémantique précise.
- Performance d'ingestion acceptable pour la population de la base vectorielle.
- Robustesse et fiabilité du stockage des vecteurs.
- Facilité d'intégration et de maintenance.
