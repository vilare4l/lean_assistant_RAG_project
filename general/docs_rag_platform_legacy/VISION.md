# PRD - RAG Platform Modulaire

## **1. Vision & Contexte**

### **Problématique identifiée**
Les solutions RAG actuelles souffrent de plusieurs limitations majeures :
- **Silos techniques** : Chaque implémentation (web crawling, traitement de documents, YouTube transcripts) nécessite des structures de BDD différentes et des adaptations constantes
- **Couplage fonctionnel** : Les processus de traitement, embedding et requêtage sont mélangés, créant des doublons et une maintenance complexe
- **Manque de standardisation** : Absence de format unifié pour gérer différents types de sources de données
- **Réinvention permanente** : Chaque nouveau projet nécessite de reconstruire l'architecture de base

### **Vision du produit**
Créer une plateforme RAG modulaire et unifiée qui permet aux organisations d'exploiter efficacement leurs bases de connaissances internes avec l'IA, tout en conservant leur souveraineté sur les données. La plateforme doit offrir une architecture découplée où chaque composant peut être utilisé indépendamment, avec un format de données standardisé qui fonctionne quelle que soit la source.

### **Objectifs business**
- **Court terme** : Créer un MVP personnel pour optimiser les activités de consultant (domaines : business général, finance, lean management, construction)
- **Moyen terme** : Développer un produit commercialisable (self-hosted et SaaS)
- **Long terme** : Offrir une alternative souveraine et performante aux solutions propriétaires du marché

## **2. Utilisateurs & Market**

### **Personas cibles**

**Persona principal - Phase MVP :**
- **Consultant indépendant** : Professionnel ayant besoin d'accéder rapidement à une base de connaissances structurée sur plusieurs domaines d'expertise pour améliorer ses prestations clients

**Personas cibles - Phase produit :**
- **Professionnels généralistes** : Managers, consultants, analystes ayant besoin d'exploiter des connaissances métier variées
- **Équipes projet** : Groupes de travail souhaitant centraliser et exploiter leur documentation interne
- **PME/ETI** : Entreprises cherchant à valoriser leur capital intellectuel sans dépendre de solutions propriétaires externes

### **Use cases principaux**
- **Consultation de base de connaissances** : Interrogation en langage naturel de documentations techniques, process métier, veille sectorielle
- **Intégration multi-sources** : Centralisation de connaissances provenant de documents, sites web, contenus vidéo dans une interface unique
- **Séparation par domaines** : Gestion cloisonnée de différents domaines d'expertise (finance, lean, construction, etc.)
- **Souveraineté des données** : Déploiement on-premise pour conserver le contrôle total sur les données sensibles

### **Positionnement concurrentiel**
- **vs Solutions propriétaires (ex: Delos)** : Alternative open-source avec possibilité de self-hosting pour la souveraineté des données
- **vs Frameworks techniques (LangChain)** : Solution clé-en-main plutôt qu'outil de développement - "mine" plutôt que "pioche"
- **vs Solutions généralistes** : Focus sur l'architecture modulaire et la standardisation des données pour éviter les silos

## **3. Architecture & Approche Technique**

### **Principes d'architecture**

**Modularité par services MCP :**
- Architecture basée sur des MCP servers indépendants communicant entre eux
- Séparation claire des responsabilités : ingestion, traitement, embedding, stockage, requêtage
- Chaque service peut être utilisé indépendamment ou en composition

**Standardisation des données :**
- Format JSON unifié en sortie de traitement, quelle que soit la source (documents, web crawling, YouTube)
- Structure de BDD standardisée compatible multi-sources
- Pipeline d'embedding unique pour toutes les sources

### **Stack technique envisagée**
- **Backend** : FastAPI, Python
- **Frontend** : React ou Vue.js
- **Base de données** : Supabase (cloud ou self-hosted)
- **Embedding** : OpenAI Embeddings
- **LLM** : Choix multiple (OpenAI, OpenRouter, modèles locaux)
- **Knowledge Graph** : Neo4j
- **Conteneurisation** : Docker/Docker Compose

### **Gestion multi-domaines**
- **Supabase Cloud** : Projets séparés par domaine utilisant le schéma public par défaut
- **Supabase Self-hosted** : Schémas différents dans la même instance
- Isolation des données par domaine sans restrictions avancées (gestion au niveau produit)
- Un utilisateur peut gérer plusieurs domaines simultanément

### **Architecture MCP - Approche évolutive**

**Phase MVP (hybride n8n/Python) :**
- **MCP Server Crawl4AI** : Python/Docker (existant, à adapter pour multi-schéma)
- **MCP Server Documents** : n8n (adaptation du workflow existant)
- **MCP Server YouTube** : n8n (adaptation du workflow existant)
- **MCP Server Media** : Python/Docker (OCR, vision AI, speech-to-text)
- **MCP Server Query** : n8n (prototypage rapide)
- **MCP Server Embedding** : Python/Docker (service unifié)
- **MCP Server Neo4j** : Python/Docker (à développer)

**Phase produit (full Python/Docker) :**
- Migration progressive des services n8n vers Python/Docker pour plus de robustesse et maintenabilité

### **MCP Server Media - Spécifications**

**Fonctionnalités :**
- **Images** : OCR (Tesseract/Cloud OCR) + description IA (GPT-4V/Claude Vision)
- **Audio** : Transcription speech-to-text (Whisper API/local)
- **Vidéos** : Extraction frames clés + transcription audio
- **Stockage** : Interface vers Cloudinary/S3/service externe
- **Output** : JSON standardisé (URL média + contenu textuel extrait)

**Architecture :**
- Service Python/Docker indépendant dès le MVP
- Queue de traitement asynchrone pour gros fichiers
- Cache des résultats de traitement IA
- Gestion des erreurs et retry automatique

## **4. Fonctionnalités Core**

### **Pipeline d'ingestion**

**Sources supportées :**
- **Web crawling** : Sites web, documentation en ligne (Crawl4AI)
- **Documents** : PDF, Word, Excel, PowerPoint, CSV, texte (tous formats)
  - *Traitement avancé des tableaux intégrés dans les PDF*
  - *Gestion performante des fichiers CSV volumineux*
- **Contenus vidéo** : Transcripts YouTube + vidéos uploadées
- **Médias** : 
  - *Images* : JPG, PNG, WebP (OCR + description IA)
  - *Audio* : MP3, WAV, M4A (transcription speech-to-text)
  - *Vidéos* : MP4, AVI, MOV (frames + audio)
- **Extensions futures** : Slack, Notion, bases de connaissances internes, messages avec médias

**Processus unifié :**
1. Ingestion de la source brute
2. Traitement et extraction du contenu (avec parsing spécialisé pour les tableaux)
3. Normalisation vers le format JSON standardisé
4. Enrichissement des métadonnées (source, date, type, structure tabulaire, etc.)

**Processus unifié médias :**
1. Upload/ingestion du fichier média
2. Stockage sur service externe (Cloudinary/S3)
3. Traitement IA selon le type (OCR, vision, transcription)
4. Normalisation vers JSON standardisé (URL + contenu textuel extrait)
5. Embedding du contenu textuel uniquement

### **Moteur d'embedding unifié**
- Service MCP dédié indépendant des sources
- Traitement du JSON standardisé quelle que soit l'origine
- Embedding OpenAI par défaut
- Architecture prête pour d'autres modèles d'embedding

### **Système de stockage multi-schéma**
- Structure de tables standardisée compatible toutes sources
- Support Supabase Cloud (projets séparés) et Self-hosted (schémas séparés)
- Gestion transparente du multi-domaine
- Integration Neo4j pour le knowledge graph

### **Moteur de requêtage**
- Interface de chat unifiée pour interroger tous les domaines
- Stratégies avancées de recherche (exemples de code existants)
- Support knowledge graph
- Requêtage indépendant par domaine (pas de mix inter-domaines)

### **Interface utilisateur**

**Phase MVP :**
- Configuration via .env et création manuelle des schémas Supabase
- Interface Slack pour l'interaction chat
- Ajout de sources au fil de l'eau via chat

**Phase produit :**
- Dashboard web d'administration des domaines
- Interface de chat intégrée
- Monitoring de l'ingestion et des performances

### **Workflows adaptables**
- Templates préconfigurés pour différents types de sources
- Personnalisation des règles de traitement
- Triggers d'ingestion configurables
- Stratégies de requêtage modulaires

## **5. Roadmap & Priorités**

### **MVP Personnel - Priorité immédiate**

**Infrastructure fondamentale :**
- **Structure Supabase unifiée** : Architecture multi-schéma compatible cloud (projets séparés) et self-hosted (schémas différents)
- **MCP Server Crawl4AI** : Adaptation de l'exemple existant pour supporter multi-schéma + suppression du requêtage (focus ingestion/embed uniquement)

**Services d'ingestion :**
- **MCP Server Documents** : Adaptation du workflow n8n existant pour traitement de tous types de documents (PDF avec tableaux, CSV, Office)
- **MCP Server YouTube** : Adaptation du workflow n8n existant pour transcripts vidéo
- **MCP Server Media** : Développement du service de traitement des médias (OCR, vision AI, speech-to-text)
- **MCP Server Neo4j** : Implémentation du knowledge graph (exemples de code disponibles)

**Service de requêtage :**
- **MCP Server Query** : Adaptation en n8n des exemples de requêtage existants
- **Interface Slack** : Intégration MCP pour interaction utilisateur

### **Version Produit**

**Migration technique :**
- Conversion progressive des services n8n vers Python/Docker pour robustesse
- Développement du dashboard web d'administration
- Interface de chat intégrée (remplacement de Slack)

**Fonctionnalités avancées :**
- Monitoring et observabilité (exploration LangSmith)
- Templates et workflows personnalisables
- Gestion utilisateurs et permissions
- API publique pour intégrations tierces

### **Version Commerciale**

**Modèles de déploiement :**
- Packaging self-hosted optimisé (Docker Compose)
- Infrastructure SaaS multi-tenant
- Documentation et support client

**Extensions fonctionnelles :**
- Connecteurs additionnels (Slack, Notion, etc.)
- Stratégies d'embedding multiples
- Support multilingue
- Conformité RGPD avancée

### **Horizon temporel**
- **MVP Personnel** : Développement au fil de la disponibilité (side project)
- **Version Produit** : Après validation MVP
- **Commercialisation** : En fonction des retours marché

## **6. Modèle de Déploiement**

### **Approche duale - Même codebase**
- Architecture unique supportant les deux modes via configuration
- Adaptation transparente selon l'environnement de déploiement
- Maintien d'une seule base de code pour simplifier le développement

### **Self-hosted**

**Architecture Docker :**
- **Docker Compose** pour orchestration simplifiée
- Services containerisés indépendants (MCP servers, bases de données, frontend)
- Volumes persistants pour données et configuration
- Réseau Docker interne pour communication inter-services

**Installation et configuration :**
- **Complexité acceptable** : `docker-compose build && docker-compose up`
- **Configuration via .env** : Variables d'environnement pour personnalisation
- **Scripts SQL fournis** : Création automatique des tables, index, fonctions, triggers
- **Setup initial** : Scripts d'initialisation des schémas multi-domaines
- **Prérequis** : Docker et Docker Compose installés
- **Public cible** : Utilisateurs techniques acceptant une approche "geek"

**Gestion des domaines :**
- Schémas Supabase multiples dans instance self-hosted
- **Scripts SQL de domaine** : Création automatique des structures par schéma
- Isolation des données par schéma

### **SaaS Cloud**

**Infrastructure multi-tenant :**
- Projets Supabase séparés par client/domaine
- Utilisation du schéma public par défaut
- **Scripts SQL standardisés** : Déploiement automatique sur nouveaux projets
- Isolation native des données par projet

**Scalabilité :**
- Services MCP déployés sur infrastructure cloud élastique
- Load balancing automatique
- Monitoring et alerting intégrés

### **Ressources SQL incluses**
- **Tables principales** : Documents, embeddings, metadata, knowledge graph
- **Index optimisés** : Performance de recherche vectorielle et textuelle
- **Fonctions Supabase** : Recherche sémantique, gestion des domaines
- **Triggers** : Audit, synchronisation, nettoyage automatique
- **Vues** : Requêtes complexes pré-optimisées
- **Scripts de migration** : Évolution de schéma entre versions

### **Migration et compatibilité**
- Export/import de données entre modes de déploiement
- Compatibilité des configurations et schémas
- Documentation de migration self-hosted ↔ SaaS

## **7. Modèle Économique**

### **Stratégie de monétisation**

**Self-hosted - Modèle de licence :**
- **Licence perpétuelle** par instance/organisation
- **Support et mises à jour** : Abonnement optionnel annuel
- **Cible** : Entreprises privilégiant la souveraineté des données
- **Avantage** : Coût prévisible, pas de dépendance usage

**SaaS Cloud - Modèle usage :**
- **Pricing basé sur la consommation** : Tokens d'embedding et requêtes LLM
- **Facturation mensuelle** selon l'utilisation réelle
- **Évolutif** avec les besoins clients
- **Transparent** : Pas de surprise sur les coûts

### **Structure de pricing envisagée**

**Freemium - Découverte du produit :**
- **1 domaine de connaissance** maximum
- **20 documents** par domaine
- **Limitations sur les requêtes** mensuelles
- **Objectif** : Permettre l'évaluation complète du produit

**Self-hosted :**
- **Licence Standard** : Prix fixe par instance
- **Support Premium** : Maintenance et support prioritaire (abonnement annuel)
- **Enterprise** : Fonctionnalités avancées + support dédié

**SaaS Cloud :**
- **Starter** : Seuils d'usage généreux avec tarif dégressif
- **Professional** : Volumes moyens avec fonctionnalités business
- **Enterprise** : Usage illimité + SLA + support dédié

### **Modèle de coûts**
- **Coûts variables principaux** : Embeddings (OpenAI) et requêtes LLM
- **Répercussion transparente** : Marge sur les coûts d'API externes
- **Optimisation** : Possibilité de modèles locaux pour réduire les coûts

### **Positionnement concurrentiel**
- **Alternative open-source** aux solutions propriétaires
- **Flexibilité déploiement** : Choix entre contrôle (self-hosted) et simplicité (SaaS)
- **Pas de vendor lock-in** : Données exportables, code accessible

## **8. Contraintes & Considérations**

### **Sécurité & Confidentialité**

**RGPD by design :**
- **Consentement** : Gestion explicite des données personnelles dans les documents
- **Droit à l'effacement** : Suppression complète des embeddings et métadonnées
- **Portabilité** : Export complet des données utilisateur
- **Minimisation** : Collecte uniquement des données nécessaires au fonctionnement

**Architecture de sécurité :**
- **Chiffrement en transit** : HTTPS/TLS pour toutes les communications
- **Chiffrement au repos** : Protection des données stockées
- **Isolation des données** : Séparation stricte par domaine/tenant
- **Authentification robuste** : JWT, 2FA pour accès admin

### **Performance & Scalabilité**

**Contraintes de performance :**
- **Temps d'ingestion acceptable** : Traitement en arrière-plan pour gros volumes
- **Réponse chat < 5s** : Optimisation des requêtes vectorielles
- **Support concurrentiel** : Architecture stateless pour scaling horizontal

**Optimisations techniques :**
- **Index vectoriels optimisés** : Performance de recherche sémantique
- **Cache intelligent** : Réponses fréquentes et embeddings récurrents
- **Processing asynchrone** : Ingestion non-bloquante
- **Monitoring ressources** : Alerting sur les goulots d'étranglement

### **Gestion des médias**

**Stockage et coûts :**
- **Séparation base/médias** : BDD contient uniquement URLs + métadonnées
- **Service externe** : Cloudinary, AWS S3, ou équivalent selon déploiement
- **Optimisation coûts** : Compression automatique, CDN pour distribution

**Performance :**
- **Processing asynchrone** : Traitement IA des médias en arrière-plan
- **Cache intelligent** : Résultats OCR/transcription stockés
- **Limites de taille** : Contraintes sur upload selon plan tarifaire

### **Compatibilité & Interopérabilité**

**Support plateforme :**
- **Containerisation Docker** : Compatibilité multi-OS (Linux, macOS, Windows)
- **Architecture cloud-native** : Déploiement Kubernetes possible
- **APIs standards** : REST/GraphQL pour intégrations tierces

**Documentation multilingue :**
- **Documentation technique en anglais** : Standard industrie
- **Interface utilisateur multilingue** : Si complexité raisonnable
- **Support international** : Gestion des encodages et fuseaux horaires

### **Métriques de succès MVP**

**Performance technique :**
- **Qualité des réponses** : Pertinence et précision des résultats
- **Facilité d'ajout de sources** : Temps et complexité d'intégration
- **Stabilité système** : Uptime et robustesse des services MCP

**Adoption utilisateur :**
- **Fréquence d'utilisation** : Engagement quotidien/hebdomadaire
- **Diversité des requêtes** : Utilisation effective des différents domaines
- **Feedback qualitatif** : Satisfaction et suggestions d'amélioration

## **9. Risques & Mitigation**

### **Risques techniques**

**Complexité de l'architecture MCP :**
- **Risque** : Courbe d'apprentissage et debugging complexe
- **Mitigation** : Démarrage hybride n8n/Python pour validation rapide, migration progressive

**Performance des embeddings :**
- **Risque** : Coûts élevés et latence avec volumes importants
- **Mitigation** : Cache intelligent, optimisation des chunks, possibilité de modèles locaux

**Fragmentation des services :**
- **Risque** : Maintenance complexe avec multiplication des MCP servers
- **Mitigation** : Documentation rigoureuse, tests d'intégration, monitoring centralisé

### **Risques produit**

**Adoption limitée du self-hosted :**
- **Risque** : Complexité technique rebutant les utilisateurs non-experts
- **Mitigation** : Scripts d'installation simplifiés, documentation détaillée, support communautaire

**Concurrence des solutions propriétaires :**
- **Risque** : Solutions établies avec budget marketing important
- **Mitigation** : Focus sur la souveraineté des données, approche open-source, pricing compétitif

### **Risques business**

**Évolution des coûts API externes :**
- **Risque** : Augmentation des tarifs OpenAI/autres fournisseurs
- **Mitigation** : Support multi-providers, modèles locaux, répercussion transparente

**Réglementation IA :**
- **Risque** : Nouvelles contraintes légales sur l'usage de l'IA
- **Mitigation** : Architecture flexible, conformité RGPD proactive, veille réglementaire

### **Risques opérationnels**

**Ressources de développement limitées :**
- **Risque** : Side project avec disponibilité variable
- **Mitigation** : Priorisation MVP claire, approche itérative, réutilisation code existant

**Support et maintenance :**
- **Risque** : Charge support croissante avec adoption
- **Mitigation** : Documentation exhaustive, communauté utilisateurs, automatisation déploiement

### **Plans de contingence**

**Fallback techniques :**
- Maintien des solutions actuelles en parallèle durant développement MVP
- Architecture modulaire permettant remplacement composants défaillants
- Backup et restauration automatisés

**Pivots possibles :**
- Focus exclusif self-hosted si SaaS trop complexe
- Concentration sur niche métier spécifique si généraliste difficile
- Offre consulting/intégration si produit packagé insuffisant

## **10. Next Steps**

### **Actions immédiates - MVP**

**Infrastructure de base :**
- **Analyser et standardiser** la structure Supabase à partir des exemples de code existants
- **Définir le format JSON unifié** en s'inspirant des implémentations actuelles
- **Adapter MCP Server Crawl4AI** : Support multi-schéma + suppression requêtage

**Développement des services :**
- **Convertir workflows n8n** en MCP servers (Documents, YouTube, Query)
- **Développer MCP Server Media** : OCR, vision AI, speech-to-text
- **Implémenter MCP Server Neo4j** à partir des exemples knowledge graph
- **Configurer interface Slack** pour interaction utilisateur

### **Validation MVP**

**Tests fonctionnels :**
- **Ingestion multi-sources** : Documents, web, YouTube, médias
- **Requêtage unifié** : Performance et pertinence des réponses
- **Gestion multi-domaines** : Isolation et switching entre domaines

**Métriques de succès :**
- Temps de traitement acceptable par type de source
- Qualité des réponses sur les domaines de connaissance cibles
- Stabilité de l'architecture MCP

### **Préparation version produit**

**Documentation technique :**
- **Spécifications APIs** MCP inter-services
- **Scripts SQL** complets (tables, index, fonctions, triggers)
- **Guide installation** Docker Compose self-hosted

**Architecture produit :**
- **Migration services n8n** vers Python/Docker
- **Dashboard web** d'administration
- **Interface chat** intégrée remplaçant Slack

### **Décisions à prendre**

**Choix techniques :**
- Service de stockage médias (Cloudinary vs S3 vs autre)
- Stratégie de nommage du projet
- Stack frontend définitive (React vs Vue)

**Positionnement produit :**
- Analyse concurrentielle approfondie
- Définition pricing détaillé
- Stratégie go-to-market