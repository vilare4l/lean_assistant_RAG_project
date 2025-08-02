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

- [X] Créer le projet FastAPI de base.
- [X] Configurer le `Dockerfile` et `requirements.txt` (inclut l'installation de Poppler).
- [X] Mettre en place les tests unitaires de base (couverture PDF, DOCX, CSV, XLSX).
- [X] Code formaté avec `black` et vérifié avec `mypy`.

### Phase 2: Implémentation du Parsing

- [X] Développer l'endpoint `/process-document/`.
- [X] Intégrer `unstructured` pour PDF et DOCX.
- [X] Implémenter la logique de `parser.py` pour router les types de fichiers.
- [X] Gérer l'extraction des tableaux via `unstructured` et `pandas`.
- [X] Assurer la création du `MCPPayload` complet.
- [ ] **Améliorer l'extraction structurée des tableaux des PDF** : Actuellement, `unstructured` avec la stratégie `hi_res` détecte les tableaux dans les PDF, mais ne parvient pas toujours à en extraire une représentation HTML structurée. Le texte brut du tableau est alors inclus dans les `content_chunks`. Il est essentiel d'explorer des options pour une extraction plus structurée des tableaux PDF (par exemple, affiner les paramètres d'`unstructured` ou envisager des bibliothèques dédiées comme `Camelot` ou `Tabula-py`).
- [ ] **Détection et référencement des images/schémas dans les PDF** : Extraire les images et schémas intégrés dans les PDF et les référencer dans le `MCPPayload` pour un traitement ultérieur par le `mcp_media_processor`.

### Phase 3: Streaming et Intégration

- [X] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [X] La distribution du `MCPPayload` vers d'autres MCPs est gérée par un orchestrateur externe (ex: n8n), donc aucune simulation d'envoi direct n'est requise pour ce MCP.

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du parsing, l'ajout de nouveaux formats de documents, et l'optimisation des performances.