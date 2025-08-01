# Architecture Globale de la Plateforme RAG

Ce document présente une vue d'ensemble de l'architecture du projet, illustrant l'interaction entre les différents composants, des agents utilisateurs aux services de traitement et de stockage des données.

```mermaid
graph TD
    %% ---- STYLING ----
    classDef agent fill:#D5E8D4,stroke:#82B366,stroke-width:2px;
    classDef mcp_ingest fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px;
    classDef mcp_core fill:#E1D5E7,stroke:#9673A6,stroke-width:2px;
    classDef mcp_query fill:#F8CECC,stroke:#B85450,stroke-width:2px;
    classDef db fill:#FFE6CC,stroke:#D79B00,stroke-width:2px;
    classDef external fill:#F5F5F5,stroke:#666,stroke-width:1px,stroke-dasharray: 5 5;

    %% ---- SUBGRAPHS ----
    subgraph "Applications Utilisateurs"
        direction LR
        agent_deep_research_crew["Agent: Deep Research Crew (CrewAI)"]:::agent
        agent_lean_assistant["Agent: Lean Assistant (App w/ Avatar)"]:::agent
    end

    subgraph "Couche Ingestion (MCP via SSE)"
        direction TB
        mcp_web_crawler["mcp_web_crawler (FastAPI/SSE)"]:::mcp_ingest
        mcp_document_processor["mcp_document_processor (FastAPI/SSE)"]:::mcp_ingest
        mcp_youtube_processor["mcp_youtube_processor (FastAPI/SSE)"]:::mcp_ingest
        mcp_media_processor["mcp_media_processor (FastAPI/SSE)"]:::mcp_ingest
    end

    subgraph "Coeur Plateforme RAG (Processeurs de Données)"
        direction TB
        mcp_vector_processor["mcp_vector_processor (Embedding & Stockage)"]:::mcp_core
        mcp_graph_enricher["mcp_graph_enricher (Extraction d'Entités)"]:::mcp_core
        mcp_query_handler["mcp_query_handler (Moteur de Requêtage)"]:::mcp_query
    end

    subgraph "Bases de Données"
        direction TB
        db_supabase["Supabase DB (Vecteurs, Métadonnées)"]:::db
        db_neo4j["Neo4j DB (Graphe d'Entités)"]:::db
    end
    
    subgraph "Services Externes"
        llm_openai["LLM Externe (OpenAI, etc)"]:::external
    end

    %% ---- CONNECTIONS ----
    %% Agents to LLM for reasoning
    agent_deep_research_crew -- "Raisonnement & Planification" --> llm_openai
    agent_lean_assistant -- "Compréhension & Dialogue" --> llm_openai

    %% Ingestion Flow
    agent_deep_research_crew -- "Lance Ingestion" --> mcp_web_crawler
    agent_deep_research_crew -- "Lance Ingestion" --> mcp_document_processor
    agent_deep_research_crew -- "Lance Ingestion" --> mcp_youtube_processor
    agent_deep_research_crew -- "Lance Ingestion" --> mcp_media_processor

    mcp_web_crawler -- "Stream MCPPayload" --> mcp_vector_processor
    mcp_web_crawler -- "Stream MCPPayload" --> mcp_graph_enricher
    mcp_document_processor -- "Stream MCPPayload" --> mcp_vector_processor
    mcp_document_processor -- "Stream MCPPayload" --> mcp_graph_enricher
    mcp_youtube_processor -- "Stream MCPPayload" --> mcp_vector_processor
    mcp_youtube_processor -- "Stream MCPPayload" --> mcp_graph_enricher
    mcp_media_processor -- "Stream MCPPayload" --> mcp_vector_processor
    mcp_media_processor -- "Stream MCPPayload" --> mcp_graph_enricher
    
    mcp_vector_processor -- "Embed & Store" --> db_supabase
    mcp_graph_enricher -- "Extrait Entités via LLM" --> llm_openai
    mcp_graph_enricher -- "Popule Graphe" --> db_neo4j

    %% Query Flow
    agent_lean_assistant -- "Requête" --> mcp_query_handler
    mcp_query_handler -- "Recherche Sémantique" --> db_supabase
    mcp_query_handler -- "Recherche Graphe" --> db_neo4j
    mcp_query_handler -- "Synthèse" --> llm_openai
    llm_openai -- "Réponse" --> mcp_query_handler
    mcp_query_handler -- "Résultat" --> agent_lean_assistant

```
