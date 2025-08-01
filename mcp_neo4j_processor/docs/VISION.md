# Vision du MCP Graph Enricher (anciennement Neo4j Processor)

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_graph_enricher` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_graph_enricher` est responsable de l'extraction d'entités et de relations à partir des `MCPPayload` reçus (provenant de toutes les sources d'ingestion) et de la population d'un graphe de connaissances Neo4j. Son but est de créer un réseau sémantique riche pour améliorer la recherche et le raisonnement.

## 2. Fonctionnalités Clés

- Réception des `MCPPayload` streamés depuis les MCPs d'ingestion.
- Utilisation de LLMs pour l'extraction d'entités nommées (NER) et l'identification de relations à partir du contenu textuel des chunks.
- Transformation des entités et relations extraites en nœuds et relations Cypher pour Neo4j.
- Population incrémentale du graphe de connaissances.
- Gestion des métadonnées des entités (source, type de document, etc.).
- Intégration avec le pipeline d'ingestion global via SSE pour un feedback en temps réel.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_graph_enricher` est un processeur de données central, recevant des `MCPPayload` de tous les MCPs d'ingestion et alimentant la base de données Neo4j. Il travaille en parallèle avec le `mcp_vector_processor`.

## 4. Critères de Succès

- Haute précision de l'extraction d'entités et de relations.
- Cohérence et qualité du graphe de connaissances généré.
- Performance d'ingestion acceptable pour la population du graphe.
- Facilité d'intégration et de maintenance.
