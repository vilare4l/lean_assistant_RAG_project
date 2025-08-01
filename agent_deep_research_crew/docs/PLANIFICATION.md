# Planification de l'Agent Deep Research Crew

Ce document détaille les étapes de développement et les tâches prioritaires pour l'agent `agent_deep_research_crew`.

## 1. Objectifs du Sprint Actuel

- Mettre en place l'environnement de développement CrewAI de base.
- Définir les premiers rôles et tâches pour l'ingestion web simple.
- Implémenter un outil pour appeler le `mcp_web_crawler`.
- Tester un workflow d'ingestion de bout en bout.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Créer le projet CrewAI de base.
- [ ] Configurer la connexion au LLM.
- [ ] Définir un agent simple avec un rôle et une tâche initiale.

### Phase 2: Implémentation de l'Ingestion Web

- [ ] Créer un outil CrewAI pour appeler l'API `/process-url/` du `mcp_web_crawler`.
- [ ] Définir une tâche pour l'agent qui utilise cet outil pour ingérer une URL.
- [ ] Mettre en place un processus CrewAI pour orchestrer cette tâche.

## 3. Dépendances

- Les MCPs d'ingestion (notamment `mcp_web_crawler`) doivent être déployés et accessibles.
- Les clés API LLM doivent être configurées.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'ajout de la gestion des documents et des médias, l'amélioration de la robustesse des workflows d'ingestion, et l'intégration de la gestion des erreurs.
