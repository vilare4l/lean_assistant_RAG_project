# Plan de Développement du MVP

## 1. Introduction et Rôle de ce Document

Ce document est la feuille de route stratégique pour le développement du **MVP (Minimum Viable Product)** de la plateforme RAG. Il sert de pont entre la vision globale définie dans `VISION.md` et les détails techniques de l'implémentation décrits dans `ARCHITECTURE.md`.

L'objectif de ce plan est de décomposer le développement en lots de travaux logiques, de clarifier l'ordre d'exécution et de suivre la progression des tâches. Chaque tâche listée ici est spécifiée en détail dans un **Product Requirements Prompt (PRP)** dédié, situé dans le dossier `docs/PRPs/`.

## 2. Stratégie de Développement par Lots

Le développement du MVP est organisé en quatre lots stratégiques. Chaque lot s'appuie sur le précédent, créant une progression logique depuis les fondations jusqu'à l'application fonctionnelle.

### Lot 1 : Les Fondations Indispensables
Ce lot constitue le socle technique du projet. Sans ces fondations, aucun service ne peut fonctionner. Nous définissons ici le contrat de données (le format JSON standard) et la structure de stockage (la base de données), qui sont les deux piliers sur lesquels reposera toute l'architecture.

### Lot 2 : Le Cœur du Traitement de Données
Une fois les fondations en place, nous développons les services MCP (Model Context Protocol) responsables de l'ingestion et du traitement des différentes sources de données. Chaque service est un micro-pipeline indépendant qui prend une source brute et la transforme en JSON standardisé, prêt à être stocké et "embeddé".

### Lot 3 : La Capacité de Requêtage
Avec une base de données peuplée de données structurées, nous pouvons maintenant construire le service qui permet de les interroger. Pour le MVP, nous utilisons une approche de prototypage rapide avec n8n pour valider le flux de requêtage sans investir immédiatement dans un service Python complet.

### Lot 4 : L'Assemblage et l'Accessibilité
Ce dernier lot consiste à assembler tous les composants pour créer un système fonctionnel et accessible. Nous configurons l'interface utilisateur (Slack) pour interagir avec le système et nous orchestrons l'environnement de développement pour que tous les services puissent être lancés et communiquent facilement entre eux.

## 3. Dépendances et Ordre d'Exécution

L'ordre des tâches n'est pas arbitraire. Voici les principales dépendances à respecter :

- **Le Lot 1 est un prérequis absolu** pour tous les autres lots.
- La **Tâche 1.2 (Format JSON)** doit idéalement être terminée avant de commencer le **Lot 2**, car tous les services d'ingestion doivent produire ce format.
- Les tâches du **Lot 2 sont largement parallélisables**. Le développement des différents serveurs MCP (Documents, YouTube, Media, etc.) peut se faire en parallèle une fois le Lot 1 terminé.
- Le **Lot 3 dépend du Lot 1 et d'au moins un service fonctionnel du Lot 2** pour avoir des données à interroger.
- Le **Lot 4 dépend de tous les autres lots**. L'orchestration ne peut se faire que lorsque tous les services sont prêts, et l'interface utilisateur a besoin du service de requêtage pour fonctionner.

## 4. Plan d'Action Détaillé

*Pour commencer une tâche, veuillez vous référer à son PRP dédié pour obtenir toutes les spécifications techniques et le contexte nécessaire.*

### **Lot 1 : Infrastructure et Fondations**
*Le socle technique du projet.*

- [X] **Tâche 1.1 : Définir la Structure de la Base de Données Unifiée**
  - **PRP** : `docs/PRPs/1.1_database_structure.md`
- [X] **Tâche 1.2 : Définir le Format de Données Standardisé**
  - **PRP** : `docs/PRPs/1.2_standardized_data_format.md`

---

### **Lot 2 : Services d'Ingestion (Cœur Python/Docker)**
*Les services de traitement des données.*

- [X] **Tâche 2.1 : Adapter le `MCP Server Crawl4AI`**
  - **PRP** : `docs/PRPs/2.1_mcp_crawl4ai_adapter.md`
- [X] **Tâche 2.2 : Développer le `MCP Server Documents`**
  - **PRP** : `docs/PRPs/2.2_mcp_documents_server.md`
- [X] **Tâche 2.3 : Développer le `MCP Server YouTube`**
  - **PRP** : `docs/PRPs/2.3_mcp_youtube_server.md`
- [X] **Tâche 2.4 : Développer le `MCP Server Media`**
  - **PRP** : `docs/PRPs/2.4_mcp_media_server.md`
- [X] **Tâche 2.5 : Développer le `MCP Server Neo4j`**
  - **PRP** : `docs/PRPs/2.5_mcp_neo4j_server.md`

---

### **Lot 3 : Service de Requêtage (Python)**
*Le cerveau de la plateforme RAG.*

- [X] **Tâche 3.1 : Développer le `MCP Server Query`**
  - **PRP** : `docs/PRPs/3.1_mcp_query_server_n8n.md`

---

### **Lot 4 : Interface et Déploiement**
*Assemblage et accessibilité du MVP.*

- [X] **Tâche 4.1 : Configurer l'Interface Utilisateur (Slack)**
  - **PRP** : `docs/PRPs/4.1_slack_interface.md`
- [X] **Tâche 4.2 : Orchestrer l'Environnement de Développement**
  - **PRP** : `docs/PRPs/4.2_dev_environment_orchestration.md`

## 5. Prochaines Étapes

Le développement doit commencer par le **Lot 1 : Infrastructure et Fondations**. La première étape concrète est de prendre connaissance du PRP de la **Tâche 1.1** et de commencer son implémentation.