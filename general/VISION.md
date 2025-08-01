# Vision Globale du Projet : Lean Assistant RAG Platform

Ce document présente la vision d'ensemble et les objectifs stratégiques du projet `Lean Assistant RAG Platform`.
Il sert de référence principale pour tous les composants et sous-projets.

## 1. Problématique Adressée

Les organisations modernes génèrent et accumulent d'énormes volumes de données non structurées (documents, médias, web) et structurées (bases de données, code). L'accès rapide, la compréhension et l'exploitation de cette connaissance sont des défis majeurs. Les solutions existantes souffrent souvent de silos d'information, d'un manque de standardisation et d'une difficulté à établir des liens sémantiques entre les différentes sources.

## 2. Vision du Produit

Créer une plateforme RAG (Retrieval-Augmented Generation) modulaire, unifiée et intelligente, capable de transformer des données brutes et hétérogènes en une base de connaissances actionnable. Cette plateforme permettra aux utilisateurs d'interroger cette connaissance de manière naturelle et d'obtenir des suggestions et des ressources pertinentes, notamment dans le domaine du Lean Management.

La plateforme sera caractérisée par :
- Une architecture découplée basée sur des microservices (MCPs).
- Un format de données standardisé (`MCPPayload`) pour toutes les sources.
- Un moteur d'ingestion robuste capable de traiter divers types de médias.
- Un **graphe de connaissances enrichi** pour capturer les entités et leurs relations à travers tous les domaines.
- Des agents intelligents pour automatiser l'ingestion et faciliter l'interaction utilisateur.

## 3. Objectifs Stratégiques

- **Optimisation de l'Accès à la Connaissance** : Permettre un accès rapide et intuitif à des informations complexes et dispersées.
- **Amélioration de la Prise de Décision** : Fournir des suggestions et des ressources basées sur une connaissance consolidée.
- **Souveraineté des Données** : Offrir des options de déploiement flexibles (self-hosted) pour un contrôle total sur les données sensibles.
- **Extensibilité et Maintenabilité** : Concevoir une architecture modulaire facilitant l'ajout de nouvelles sources, de nouveaux modèles et de nouvelles fonctionnalités.

## 4. Utilisateurs Cibles

- **Agent: Deep Research Crew** : L'équipe IA autonome chargée de la constitution et de l'enrichissement de la base de connaissances RAG.
- **Agent: Lean Assistant** : L'application utilisateur interactive (avec avatar et lecture vocale) qui interagit avec la plateforme pour obtenir des suggestions et des ressources sur des problèmes business.
- **Développeurs/Administrateurs** : Ceux qui déploient, maintiennent et étendent la plateforme.

## 5. Composants Clés de la Plateforme

- **Agents Intelligents** : `agent_deep_research_crew` (ingestion) et `agent_lean_assistant` (requêtage/interaction).
- **Microservices MCP d'Ingestion** : `mcp_document_processor`, `mcp_media_processor`, `mcp_web_crawler`, `mcp_youtube_processor`.
- **Microservices MCP de Traitement Central** : `mcp_vector_processor` (embeddings) et `mcp_graph_enricher` (extraction d'entités pour Neo4j).
- **Microservice MCP de Requêtage** : `mcp_query_handler` (orchestre la recherche et la synthèse).
- **Bases de Données** : Supabase (PostgreSQL avec `pg_vector`) pour les embeddings et les métadonnées, Neo4j pour le graphe de connaissances.
- **Services LLM Externes** : Pour la génération d'embeddings, l'extraction d'entités, le raisonnement et la synthèse de réponses.

## 6. Prochaines Étapes

Ce document de vision sera complété par un plan de planification détaillé (`PLANIFICATION.md`) et des documents de spécification pour chaque microservice et agent.
