# Architecture du MCP Document Processor

Ce document détaille l'architecture technique du microservice `mcp_document_processor`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (avec support SSE pour le streaming des résultats)
- **Librairies de Traitement** : `unstructured` pour l'extraction de texte et de tableaux, `pandas` pour la manipulation de données tabulaires, `openpyxl` pour les fichiers Excel.
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint `/process-document/`** : Reçoit les fichiers à traiter.
- **Module `parser.py`** : Contient la logique de routage vers les parsers spécifiques en fonction du type MIME du document.
- **Parsers Spécifiques** : Fonctions ou classes dédiées à l'extraction de contenu pour chaque format (ex: PDF, DOCX, CSV, XLSX).
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py` pour la structure des données entrantes et sortantes.

## 3. Flux de Données

1. Un agent (ex: `Deep Research Crew`) envoie un fichier au `mcp_document_processor` via l'endpoint `/process-document/`.
2. Le `mcp_document_processor` lit le fichier et détermine son type MIME.
3. Le fichier est routé vers le parser approprié (`unstructured` pour PDF/DOCX, `pandas` pour CSV/XLSX).
4. Le contenu est extrait et transformé en `Chunk` et `TabularData`.
5. Un `MCPPayload` est construit avec les informations de la source, les chunks et les données tabulaires.
6. Le `MCPPayload` est streamé (via SSE) vers le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des fichiers pour ne pas bloquer l'API.
- Optimisation des parsers pour gérer de gros volumes de données.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
