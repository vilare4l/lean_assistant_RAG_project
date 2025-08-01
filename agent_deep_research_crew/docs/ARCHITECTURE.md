# Architecture de l'Agent Deep Research Crew

Ce document détaille l'architecture technique de l'agent `agent_deep_research_crew`.

## 1. Stack Technique

- **Framework d'Agent** : CrewAI
- **Langage** : Python
- **LLM** : Connecté à un LLM externe pour le raisonnement et la génération de tâches.
- **Communication avec MCPs** : Utilisation des APIs (REST/SSE) des microservices MCP d'ingestion.

## 2. Composants Principaux

- **Agents CrewAI** : Définition des rôles, des outils et des objectifs de chaque agent au sein de l'équipe.
- **Outils (Tools)** : Implémentation des outils permettant aux agents d'interagir avec les MCPs d'ingestion (ex: `WebCrawlerTool`, `DocumentProcessorTool`).
- **Processus (Process)** : Définition des workflows et des étapes que l'équipe d'agents doit suivre pour accomplir sa mission.

## 3. Flux de Données

1. L'agent reçoit une mission (ex: "Ingérer la documentation sur le Lean Manufacturing").
2. Il utilise son LLM pour décomposer la mission en tâches et planifier les actions.
3. Les agents CrewAI utilisent leurs outils pour appeler les MCPs d'ingestion (ex: `mcp_web_crawler` pour des URLs, `mcp_document_processor` pour des fichiers).
4. Les MCPs traitent les données et streament les `MCPPayload` vers les processeurs de données (vectoriel et graphe).
5. L'agent surveille le succès de l'ingestion et gère les éventuelles erreurs.

## 4. Considérations de Performance et Scalabilité

- Optimisation des interactions LLM pour réduire les coûts et la latence.
- Gestion asynchrone des appels aux MCPs.
- Possibilité de paralléliser les tâches d'ingestion.
