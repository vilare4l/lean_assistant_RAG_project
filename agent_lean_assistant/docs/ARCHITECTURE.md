# Architecture de l'Agent Lean Assistant

Ce document détaille l'architecture technique de l'agent `agent_lean_assistant`.

## 1. Stack Technique

- **Langage** : Python (ou autre, à définir selon le choix de l'interface utilisateur).
- **Interface Utilisateur** : Framework UI (ex: Streamlit, Gradio, ou un framework web/desktop plus complet).
- **Interaction Vocale** : Librairies Speech-to-Text (STT) et Text-to-Speech (TTS).
- **LLM** : Connecté à un LLM externe pour la compréhension du langage naturel et la génération de dialogue.
- **Communication avec MCP** : Utilisation de l'API (REST) du `mcp_query_handler`.

## 2. Composants Principaux

- **Module d'Interface Utilisateur** : Gère l'affichage, les interactions et l'avatar.
- **Module d'Interaction Vocale** : Intègre les fonctionnalités STT et TTS.
- **Module de Requêtage** : Formule les requêtes pour le `mcp_query_handler` et traite les réponses.
- **Module de Dialogue** : Gère la conversation avec l'utilisateur, potentiellement via un LLM.

## 3. Flux de Données

1. L'utilisateur pose un problème business via l'interface vocale ou textuelle.
2. La requête est traitée (STT si vocal) et envoyée au `mcp_query_handler`.
3. Le `mcp_query_handler` recherche les informations pertinentes et renvoie une réponse.
4. La réponse est affichée à l'utilisateur et lue vocalement (TTS).
5. Le module de dialogue maintient le contexte de la conversation.

## 4. Considérations de Performance et Scalabilité

- Optimisation de la latence pour une expérience utilisateur fluide.
- Choix de librairies STT/TTS performantes.
- Gestion efficace des appels au `mcp_query_handler` et au LLM.
- Possibilité de déployer l'application de manière scalable (web, desktop).
