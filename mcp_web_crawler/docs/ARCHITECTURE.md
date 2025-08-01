# Architecture du MCP Web Crawler

Ce document détaille l'architecture technique du microservice `mcp_web_crawler`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (avec support SSE pour le streaming des résultats)
- **Librairies de Traitement** : `crawl4ai` pour le crawling et l'extraction de contenu, `openai` pour la génération de résumés de code.
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint `/process-url/`** : Reçoit les URLs à crawler.
- **Module `processor.py`** : Orchestre le processus de crawling, d'extraction et de chunking.
- **Module `utils.py`** : Contient les fonctions utilitaires pour le chunking intelligent, l'extraction de blocs de code et la génération de résumés.
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py` pour la structure des données entrantes et sortantes.

## 3. Flux de Données

1. Un agent (ex: `Deep Research Crew`) envoie une URL au `mcp_web_crawler` via l'endpoint `/process-url/`.
2. Le `mcp_web_crawler` utilise `crawl4ai` pour récupérer le contenu de la page web et le convertir en Markdown.
3. Le contenu Markdown est chunké intelligemment, les blocs de code sont extraits et résumés (via LLM).
4. Un `MCPPayload` est construit avec les informations de la source et les chunks de texte/code.
5. Le `MCPPayload` est streamé (via SSE) vers le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des requêtes de crawling.
- Optimisation du chunking pour minimiser les appels LLM et maximiser la pertinence.
- Gestion des caches de crawling pour éviter de retraiter les mêmes URLs.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
