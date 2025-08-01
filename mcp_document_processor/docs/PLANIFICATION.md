# Planification du MCP Document Processor

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_document_processor`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des documents.
- Intégrer la librairie `unstructured` pour le parsing de base des PDF et DOCX.
- Assurer la conversion des données extraites au format `MCPPayload`.
- Mettre en place un mécanisme de streaming (SSE) pour l'envoi du `MCPPayload`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation du Parsing

- [ ] Développer l'endpoint `/process-document/`.
- [ ] Intégrer `unstructured` pour PDF et DOCX.
- [ ] Implémenter la logique de `parser.py` pour router les types de fichiers.
- [ ] Gérer l'extraction des tableaux via `unstructured` et `pandas`.
- [ ] Assurer la création du `MCPPayload` complet.

### Phase 3: Streaming et Intégration

- [ ] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [ ] Simuler l'envoi vers le `mcp_vector_processor` et le `mcp_graph_enricher` (pour les tests).

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du parsing, l'ajout de nouveaux formats de documents, et l'optimisation des performances.
