# Planification du MCP Graph Enricher (anciennement Neo4j Processor)

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_graph_enricher`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des streams SSE.
- Intégrer les appels LLM pour l'extraction d'entités/relations.
- Mettre en place la connexion et la population de base de Neo4j.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation de l'Extraction et Population du Graphe

- [ ] Développer l'endpoint de réception des streams SSE.
- [ ] Implémenter la logique de `processor.py` pour orchestrer l'extraction.
- [ ] Développer `llm_client.py` pour les appels LLM (extraction d'entités/relations).
- [ ] Développer `graph_writer.py` pour la conversion en Cypher et l'interaction avec Neo4j.
- [ ] Assurer la population incrémentale du graphe.

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les clés API LLM doivent être configurées.
- Une instance Neo4j doit être accessible.
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de la qualité de l'extraction, la gestion des schémas de graphe complexes, et l'optimisation des performances.
