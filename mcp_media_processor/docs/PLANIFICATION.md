# Planification du MCP Media Processor

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_media_processor`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des fichiers médias.
- Intégrer les clients OpenAI (Whisper pour l'audio, Vision pour les images).
- Assurer la conversion des données extraites au format `MCPPayload`.
- Mettre en place un mécanisme de streaming (SSE) pour l'envoi du `MCPPayload`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation du Traitement Média

- [ ] Développer l'endpoint `/process-media/`.
- [ ] Implémenter la logique de `processor.py` pour orchestrer le traitement.
- [ ] Développer `clients.py` pour les appels aux APIs OpenAI.
- [ ] Gérer l'upload simulé ou réel des médias.
- [ ] Assurer la création du `MCPPayload` complet avec les données extraites.

### Phase 3: Streaming et Intégration

- [ ] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [ ] Simuler l'envoi vers le `mcp_vector_processor` et le `mcp_graph_enricher` (pour les tests).

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les clés API OpenAI doivent être configurées.
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du traitement, l'ajout de nouveaux formats médias, et l'optimisation des performances.
