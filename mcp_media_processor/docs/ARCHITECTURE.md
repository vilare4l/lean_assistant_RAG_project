# Architecture du MCP Media Processor

Ce document détaille l'architecture technique du microservice `mcp_media_processor`.

## 1. Stack Technique

- **Langage** : Python
- **Framework API** : FastAPI (avec support SSE pour le streaming des résultats)
- **Librairies de Traitement** : `openai` (pour Whisper et Vision API), `boto3` (pour l'intégration S3/Cloudinary si nécessaire).
- **Conteneurisation** : Docker

## 2. Composants Principaux

- **Endpoint `/process-media/`** : Reçoit les fichiers médias à traiter.
- **Module `processor.py`** : Orchestre le traitement du fichier média, incluant l'upload (simulé ou réel) et l'appel aux clients IA.
- **Module `clients.py`** : Contient les fonctions d'appel aux APIs externes (OpenAI Whisper pour l'audio, OpenAI Vision pour les images).
- **Modèles de Données** : Utilisation des schémas Pydantic définis dans `shared/schemas/mcp_payload.py` pour la structure des données entrantes et sortantes.

## 3. Flux de Données

1. Un agent (ex: `Deep Research Crew`) envoie un fichier média au `mcp_media_processor` via l'endpoint `/process-media/`.
2. Le `mcp_media_processor` lit le fichier, détermine son type MIME et simule (ou effectue) son upload vers un stockage externe pour obtenir une URL stable.
3. Le fichier est envoyé à l'API IA appropriée (Whisper pour l'audio, Vision pour l'image) via `clients.py`.
4. Le texte extrait (transcription, description) est transformé en `Chunk`.
5. Un `MCPPayload` est construit avec les informations de la source et les chunks.
6. Le `MCPPayload` est streamé (via SSE) vers le `mcp_vector_processor` et le `mcp_graph_enricher`.

## 4. Considérations de Performance et Scalabilité

- Traitement asynchrone des fichiers pour ne pas bloquer l'API.
- Gestion des fichiers temporaires pour les APIs qui nécessitent un chemin de fichier.
- Optimisation des appels aux APIs externes pour minimiser la latence.
- Possibilité de déployer plusieurs instances du service pour la scalabilité horizontale.
