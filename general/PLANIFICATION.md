# Planification Générale du Projet : Lean Assistant RAG Platform

Ce document présente la feuille de route de haut niveau pour le développement de la `Lean Assistant RAG Platform`. Il décompose le projet en phases logiques et identifie les dépendances clés.

## 1. Approche Générale

Le développement sera mené de manière itérative, en se concentrant sur la mise en place des fondations, puis l'implémentation progressive des fonctionnalités d'ingestion, de traitement, de requêtage et enfin des agents utilisateurs.

## 2. Phases de Développement

### Phase 1: Fondations et Contrats

**Objectif** : Établir les bases techniques et les contrats de données pour l'ensemble de la plateforme.

- [ ] **Définition et Stabilisation du `MCPPayload`** : Assurer que le schéma `shared/schemas/mcp_payload.py` est complet et répond aux besoins de tous les MCPs.
- [ ] **Définition des Schémas de Base de Données** : Finaliser `shared/database_schemas/postgresql_schema.sql` et `shared/database_schemas/neo4j_schema.cypher`.
- [ ] **Mise en place de l'Environnement de Développement Global** : Docker Compose pour orchestrer les services.

### Phase 2: Services d'Ingestion (MCP Ingest)

**Objectif** : Implémenter les microservices responsables de la collecte et de la transformation des données brutes en `MCPPayload`.

- [ ] **`mcp_document_processor`** : Traitement des PDF, DOCX, CSV, XLSX.
- [ ] **`mcp_media_processor`** : Traitement des images et audio (OCR, STT, Vision).
- [ ] **`mcp_web_crawler`** : Crawling de pages web.
- [ ] **`mcp_youtube_processor`** : Extraction de transcriptions YouTube.

### Phase 3: Coeur de la Plateforme RAG (Processeurs de Données)

**Objectif** : Développer les services centraux pour la vectorisation et l'enrichissement du graphe de connaissances.

- [ ] **`mcp_vector_processor`** : Génération et stockage des embeddings dans Supabase.
- [ ] **`mcp_graph_enricher`** : Extraction d'entités/relations et population de Neo4j.

### Phase 4: Moteur de Requêtage

**Objectif** : Implémenter le service capable d'interroger la base de connaissances consolidée.

- [ ] **`mcp_query_handler`** : Orchestration de la recherche sémantique et graphe, et synthèse de réponses via LLM.

### Phase 5: Agents Utilisateurs

**Objectif** : Développer les interfaces intelligentes pour l'interaction avec la plateforme.

- [ ] **`agent_deep_research_crew`** : Agent autonome pour l'ingestion continue.
- [ ] **`agent_lean_assistant`** : Application interactive pour l'utilisateur final.

## 3. Dépendances Clés

- La Phase 1 est un prérequis pour toutes les autres phases.
- Les MCPs d'ingestion (Phase 2) peuvent être développés en parallèle, mais nécessitent la Phase 1.
- Les processeurs de données (Phase 3) nécessitent les MCPs d'ingestion pour recevoir des données.
- Le moteur de requêtage (Phase 4) nécessite les processeurs de données pour fonctionner.
- Les agents utilisateurs (Phase 5) nécessitent les services sous-jacents pour interagir.

## 4. Prochaines Étapes

Ce document sera affiné avec des détails de sprint pour chaque phase. Les spécifications détaillées de chaque microservice et agent se trouvent dans leurs dossiers respectifs.
