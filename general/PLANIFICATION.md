# Planification Générale du Projet : Lean Assistant RAG Platform

Ce document présente la feuille de route de haut niveau pour le développement de la `Lean Assistant RAG Platform`. Il décompose le projet en phases logiques et identifie les dépendances clés.

## 1. Approche Générale

Le développement sera mené de manière itérative et sera piloté par des **PRPs (Product Requirements Prompts)**. Chaque tâche de développement majeure devra être définie dans un fichier `.md` dans le dossier `/PRPs` avant de commencer l'implémentation. Ce fichier servira de cahier des charges complet pour l'agent IA.

## 2. Phases de Développement

### Phase 1: Fondations et Contrats

**Objectif** : Établir les bases techniques et les contrats de données pour l'ensemble de la plateforme.

- [X] **Définition et Stabilisation du `MCPPayload`** : `shared/schemas/mcp_payload.py`.
- [X] **Définition des Schémas de Base de Données** : `shared/database_schemas/`.
- [ ] **Mise en place de l'Environnement de Développement Global** : Docker Compose pour orchestrer les services.

### Phase 2: Services d'Ingestion (MCP Ingest)

**Objectif** : Implémenter les microservices responsables de la collecte et de la transformation des données brutes en `MCPPayload`.

- [X] **PRP pour `mcp_document_processor`** : Traitement des PDF, DOCX, CSV, XLSX.
  - [X] Code formaté avec `black` et vérifié avec `mypy`.
- [ ] **PRP pour `mcp_media_processor`** : Traitement des images et audio (OCR, STT, Vision).
- [ ] **PRP pour `mcp_web_crawler`** : Crawling de pages web.
- [ ] **PRP pour `mcp_youtube_processor`** : Extraction de transcriptions YouTube.

### Phase 3: Coeur de la Plateforme RAG (Processeurs de Données)

**Objectif** : Développer les services centraux pour la vectorisation et l'enrichissement du graphe de connaissances.

- [ ] **PRP pour `mcp_vector_processor`** : Génération et stockage des embeddings dans Supabase.
- [ ] **PRP pour `mcp_graph_enricher`** : Extraction d'entités/relations et population de Neo4j.

### Phase 4: Moteur de Requêtage

**Objectif** : Implémenter le service capable d'interroger la base de connaissances consolidée.

- [ ] **PRP pour `mcp_query_handler`** : Orchestration de la recherche sémantique et graphe, et synthèse de réponses via LLM.

### Phase 5: Agents Utilisateurs

**Objectif** : Développer les interfaces intelligentes pour l'interaction avec la plateforme.

- [ ] **PRP pour `agent_deep_research_crew`** : Agent autonome pour l'ingestion continue.
- [ ] **PRP pour `agent_lean_assistant`** : Application interactive pour l'utilisateur final.

## 3. Dépendances Clés

- La Phase 1 est un prérequis pour toutes les autres phases.
- Chaque tâche des phases 2 à 5 doit être précédée par la création et la validation de son PRP correspondant.

## 4. Prochaines Étapes

La prochaine étape est de créer le premier PRP pour le `mcp_document_processor`.