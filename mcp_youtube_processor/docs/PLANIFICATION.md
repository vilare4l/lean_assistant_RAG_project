# Planification du MCP YouTube Processor

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_youtube_processor`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des URLs YouTube.
- Intégrer la librairie `youtube-transcript-api`.
- Assurer la conversion des transcriptions au format `MCPPayload`.
- Mettre en place un mécanisme de streaming (SSE) pour l'envoi du `MCPPayload`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation du Traitement YouTube

- [ ] Développer l'endpoint `/process-youtube/`.
- [ ] Implémenter la logique de `processor.py` pour l'extraction d'ID, la récupération de transcription et le chunking.
- [ ] Gérer les cas d'erreur (URL invalide, pas de transcription).
- [ ] Assurer la création du `MCPPayload` complet avec les données de transcription.

### Phase 3: Streaming et Intégration

- [ ] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [ ] Simuler l'envoi vers le `mcp_vector_processor` et le `mcp_graph_enricher` (pour les tests).

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du traitement, la gestion des langues de transcription, et l'optimisation des performances.
