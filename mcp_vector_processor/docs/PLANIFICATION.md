# Planification du MCP Vector Processor

Ce document détaille les étapes de développement et les tâches prioritaires pour le microservice `mcp_vector_processor`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement local.
- Implémenter l'endpoint FastAPI pour la réception des streams SSE.
- Intégrer les appels aux modèles d'embedding (OpenAI).
- Mettre en place la connexion et le stockage de base dans Supabase (pg_vector).

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet FastAPI de base.
- [ ] Configurer le `Dockerfile` et `requirements.txt`.
- [ ] Mettre en place les tests unitaires de base.

### Phase 2: Implémentation de la Génération et du Stockage des Embeddings

- [ ] Développer l'endpoint de réception des streams SSE.
- [ ] Implémenter la logique de `processor.py` pour orchestrer la génération et le stockage.
- [ ] Développer `llm_client.py` pour les appels aux modèles d'embedding.
- [ ] Développer `db_client.py` pour l'interaction avec Supabase (insertion de vecteurs).
- [ ] Assurer la gestion des métadonnées lors du stockage.

## 3. Dépendances

- Le schéma `MCPPayload` doit être stable et accessible (via le dossier `shared`).
- Les clés API LLM doivent être configurées.
- Une instance Supabase avec pg_vector activé doit être accessible.
- Les outils de conteneurisation (Docker) doivent être fonctionnels.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'optimisation des performances d'embedding, la gestion des mises à jour/suppressions de documents, et l'ajout de support pour d'autres modèles d'embedding.
