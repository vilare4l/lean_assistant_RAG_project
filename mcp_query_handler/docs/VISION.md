# Vision du MCP Query Handler

Ce document décrit la vision et les objectifs spécifiques du microservice `mcp_query_handler` au sein de la plateforme RAG.

## 1. Objectif Principal

Le `mcp_query_handler` est le point d'entrée principal pour les requêtes utilisateur. Il est responsable d'orchestrer la recherche d'informations pertinentes dans les bases de données vectorielles et le graphe de connaissances, puis de synthétiser une réponse cohérente et utile en utilisant un LLM.

## 2. Fonctionnalités Clés

- Réception des requêtes utilisateur (texte libre).
- Routage intelligent des requêtes vers la base de données vectorielle (pour la recherche sémantique) et/ou le graphe de connaissances (pour la recherche d'entités et de relations).
- Récupération du contexte pertinent à partir des bases de données.
- Utilisation d'un LLM pour synthétiser une réponse à partir de la requête et du contexte récupéré.
- Gestion des requêtes complexes nécessitant une combinaison de recherche sémantique et de graphe.
- Intégration avec les agents utilisateurs (ex: `Lean Assistant`) pour fournir des réponses.

## 3. Positionnement dans l'Architecture Globale

Le `mcp_query_handler` est le cerveau de la plateforme RAG, agissant comme un orchestrateur entre les agents utilisateurs, les bases de données et les LLMs. Il est le service qui transforme une question en une réponse actionable.

## 4. Critères de Succès

- Pertinence et précision des réponses générées.
- Faible latence pour les requêtes utilisateur.
- Capacité à gérer des requêtes complexes et ambiguës.
- Robustesse et fiabilité du processus de recherche et de synthèse.
- Facilité d'intégration avec différentes interfaces utilisateur.
