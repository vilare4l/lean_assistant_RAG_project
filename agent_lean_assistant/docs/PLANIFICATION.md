# Planification de l'Agent Lean Assistant

Ce document détaille les étapes de développement et les tâches prioritaires pour l'agent `agent_lean_assistant`.

## 1. Objectifs du Sprint Actuel

- Mettre en place une interface utilisateur de base (textuelle).
- Implémenter la connexion au `mcp_query_handler`.
- Afficher les réponses du `mcp_query_handler`.

## 2. Tâches Détaillées

### Phase 1: Initialisation et Setup

- [ ] Choisir un framework UI initial (ex: Streamlit pour un prototype rapide).
- [ ] Créer le projet de base.
- [ ] Configurer la connexion au LLM (pour le dialogue).

### Phase 2: Implémentation de l'Interaction de Base

- [ ] Développer l'interface utilisateur textuelle pour la saisie de requêtes.
- [ ] Implémenter le client pour appeler l'API `/query/` du `mcp_query_handler`.
- [ ] Afficher les réponses du `mcp_query_handler` dans l'interface.

### Phase 3: Interaction Vocale (Future)

- [ ] Intégrer une librairie Speech-to-Text.
- [ ] Intégrer une librairie Text-to-Speech.
- [ ] Développer l'avatar visuel.

## 3. Dépendances

- Le `mcp_query_handler` doit être déployé et accessible.
- Les clés API LLM doivent être configurées.

## 4. Prochaines Étapes

Après ce sprint, nous nous concentrerons sur l'amélioration de l'interface utilisateur, l'intégration vocale, et l'enrichissement de l'expérience de dialogue.
