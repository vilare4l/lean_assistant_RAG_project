# Planification du MCP Document Processor

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_document_processor`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter les outils MCP spécifiques pour chaque type de document.
- Assurer la conversion des données extraites au format `MCPPayload`.
- Mettre en place un mécanisme de streaming (SSE) pour l'envoi du `MCPPayload`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [X] Créer le projet FastMCP de base.
- [X] Configurer le `Dockerfile` et `pyproject.toml` (inclut l'installation des dépendances système et Python).
- [X] Mettre en place les tests unitaires pour chaque outil MCP (PDF, DOCX, CSV, XLSX, JSON).
- [X] Code formaté avec `black` et vérifié avec `mypy`.

### Phase 2: Implémentation des Outils de Parsing

- [X] Développer l'outil MCP `process_pdf`.
- [X] Développer l'outil MCP `process_docx`.
- [X] Développer l'outil MCP `process_csv`.
- [X] Développer l'outil MCP `process_xlsx`.
- [X] Développer l'outil MCP `process_json`.
- [X] Intégrer `unstructured` pour PDF et DOCX (logique déplacée dans `tools/`).
- [X] Gérer l'extraction des tableaux via `unstructured` et `pandas` (logique déplacée dans `tools/`).
- [X] Assurer la création du `MCPPayload` complet pour tous les types de documents.
- [ ] **Amélioration CRITIQUE des fonctionnalités PDF** : Actuellement, l'extraction de contenu structuré (notamment les tableaux) des PDF est basique. Il est essentiel d'explorer et d'implémenter des solutions robustes pour :
    - Une extraction plus précise du texte et des métadonnées.
    - Une extraction structurée et fiable des tableaux (par exemple, affiner les stratégies `unstructured`, ou intégrer des bibliothèques dédiées comme `Camelot` ou `Tabula-py`).
    - Une meilleure gestion des PDF complexes (scannés, avec des mises en page non standard).
- [ ] **Détection et référencement des images/schémas dans les PDF** : Extraire les images et schémas intégrés dans les PDF et les référencer dans le `MCPPayload` pour un traitement ultérieur par le `mcp_media_processor`.

### Phase 3: Streaming et Intégration

- [X] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [X] La distribution du `MCPPayload` vers d'autres MCPs est gérée par un orchestrateur externe (ex: n8n), donc aucune simulation d'envoi direct n'est requise pour ce MCP.

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du parsing, l'ajout de nouveaux formats de documents (si nécessaire), et l'optimisation des performances.
