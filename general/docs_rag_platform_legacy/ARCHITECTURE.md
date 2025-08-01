# Architecture Technique

## 1. Stack Technique

- **Backend** : FastAPI, Python
- **Frontend** : React ou Vue.js
- **Base de données** : Supabase (cloud ou self-hosted)
- **Embedding** : OpenAI Embeddings (par défaut, avec une architecture ouverte à d'autres modèles)
- **LLM** : Choix multiple (OpenAI, OpenRouter, modèles locaux)
- **Knowledge Graph** : Neo4j
- **Conteneurisation** : Docker/Docker Compose

## 2. Gestion Multi-Domaines

L'architecture supporte l'isolation des données par domaine de connaissance, avec deux modes de déploiement :

- **Supabase Cloud** : Chaque domaine est géré dans un projet Supabase séparé, utilisant le schéma `public` par défaut. L'isolation est assurée au niveau du projet.

- **Supabase Self-hosted** : Tous les domaines sont dans la même instance Supabase, mais chaque domaine utilise un schéma PostgreSQL distinct. L'isolation est assurée au niveau du schéma.

## 3. Model Context Protocol (MCP)

Le "Model Context Protocol" (MCP) est le cœur de la plateforme. Il s'agit d'un ensemble de services spécialisés (serveurs MCP) qui articulent les fonctionnalités du système. Chaque serveur est un composant modulaire avec une responsabilité unique.

### Approche Évolutive

L'architecture MCP est conçue pour évoluer, en commençant par un MVP (Minimum Viable Product) hybride qui utilise une combinaison de services Python/Docker robustes et de workflows n8n pour un prototypage rapide.

#### Phase MVP (Hybride n8n/Python)

- **MCP Server Crawl4AI** : Python/Docker (basé sur un exemple existant, à adapter pour le multi-schéma)
- **MCP Server Documents** : n8n (adaptation d'un workflow existant)
- **MCP Server YouTube** : n8n (adaptation d'un workflow existant)
- **MCP Server Media** : Python/Docker (OCR, vision AI, speech-to-text)
- **MCP Server Query** : n8n (prototypage rapide)
- **MCP Server Embedding** : Python/Docker (service unifié)
- **MCP Server Neo4j** : Python/Docker (à développer)

#### Phase Produit (Full Python/Docker)

L'objectif à terme est de migrer progressivement tous les services n8n vers des implémentations Python/Docker pour améliorer la robustesse, la performance et la maintenabilité de la plateforme.