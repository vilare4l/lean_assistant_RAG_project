# Planification du MCP Web Crawler

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_web_crawler`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des URLs.
- Intégrer la librairie `crawl4ai` pour le crawling de base.
- Assurer la conversion du contenu web au format `MCPPayload`.
- Mettre en place un mécanisme de streaming (SSE) pour l'envoi du `MCPPayload`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation du Crawling et Traitement

- [ ] Développer l'endpoint `/process-url/`.
- [ ] Intégrer `crawl4ai` et configurer ses options.
- [ ] Implémenter la logique de `processor.py` pour orchestrer le crawling et le chunking.
- [ ] Développer `utils.py` pour le chunking intelligent et l'extraction de code.
- [ ] Assurer la création du `MCPPayload` complet avec les données web.

### Phase 3: Streaming et Intégration

- [ ] Mettre en place le streaming SSE pour l'envoi du `MCPPayload`.
- [ ] Simuler l'envoi vers le `mcp_vector_processor` et le `mcp_graph_enricher` (pour les tests).

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les clés API OpenAI (pour les résumés de code) doivent être configurées.
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la robustesse du crawling, la gestion des erreurs (ex: pages non trouvées), et l'optimisation des performances.
