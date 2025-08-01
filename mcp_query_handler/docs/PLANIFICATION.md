# Planification du MCP Query Handler

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_query_handler`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des requêtes.
- Intégrer les appels aux bases de données (Supabase et Neo4j).
- Mettre en place la synthèse de réponse via un LLM.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation du Moteur de Requêtage

- [ ] Développer l'endpoint `/query/`.
- [ ] Implémenter la logique de `processor.py` pour orchestrer la recherche.
- [ ] Développer `llm_client.py` pour la génération d'embeddings et la synthèse LLM.
- [ ] Développer `db_clients.py` pour l'interaction avec Supabase et Neo4j.
- [ ] Gérer le routage des requêtes (sémantique vs graphe).

## 3. Dépendances

- Les bases de données Supabase et Neo4j doivent être accessibles et peuplées.
- Les clés API LLM doivent être configurées.
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la pertinence des réponses, l'optimisation des performances, et l'ajout de stratégies de recherche plus avancées.
