# Vision de l'Agent Lean Assistant

Ce document décrit la vision et les objectifs de l'agent `agent_lean_assistant`.

## 1. Objectif Principal

L'agent `agent_lean_assistant` est une application utilisateur interactive (avec avatar et lecture vocale) qui fournit des suggestions intelligentes et des ressources inspirantes provenant de la base de connaissances RAG, en réponse à des problèmes business spécifiques.

## 2. Fonctionnalités Clés

- Interface utilisateur intuitive avec avatar visuel.
- Interaction vocale (Speech-to-Text pour l'entrée, Text-to-Speech pour la sortie).
- Compréhension des problèmes business et formulation de requêtes pertinentes pour le `mcp_query_handler`.
- Présentation claire et concise des suggestions et des ressources trouvées.
- Capacité à naviguer dans les résultats et à explorer les relations dans le graphe de connaissances.

## 3. Positionnement dans l'Architecture Globale

L'agent `agent_lean_assistant` est la principale interface utilisateur de la plateforme RAG. Il interagit avec le `mcp_query_handler` pour obtenir des réponses et utilise un LLM pour la compréhension du langage naturel et la génération de dialogue.

## 4. Critères de Succès

- Expérience utilisateur fluide et engageante.
- Pertinence et utilité des suggestions et ressources fournies.
- Faible latence de réponse pour une interaction naturelle.
- Facilité d'utilisation et d'adoption par les utilisateurs finaux.
