# core/mcp-servers/neo4j-processor/graph_writer.py

import os
from neo4j import AsyncGraphDatabase

# Récupérer les informations de connexion depuis les variables d'environnement
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

_driver = None

async def get_driver():
    """Initialise et retourne le driver Neo4j."""
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver

async def close_driver():
    """Ferme la connexion du driver."""
    global _driver
    if _driver:
        await _driver.close()
        _driver = None

async def populate_graph_from_analysis(repo_name: str, analysis_results: list[dict]) -> dict:
    """
    Peuple la base de données Neo4j à partir des résultats de l'analyse AST.
    """
    driver = await get_driver()
    stats = {'classes': 0, 'functions': 0, 'relations': 0}

    async with driver.session() as session:
        # 1. Créer le nœud principal pour le dépôt
        await session.run("MERGE (r:Repository {name: $repo_name})", repo_name=repo_name)

        for file_analysis in analysis_results:
            # 2. Créer le nœud pour le fichier
            await session.run(
                "MATCH (r:Repository {name: $repo_name}) "
                "MERGE (f:File {path: $path, repo_name: $repo_name}) "
                "MERGE (r)-[:CONTAINS]->(f)",
                repo_name=repo_name, path=file_analysis['file_path']
            )
            
            # 3. Créer les nœuds pour les classes et les fonctions
            for class_info in file_analysis['classes']:
                await session.run(
                    "MATCH (f:File {path: $path, repo_name: $repo_name}) "
                    "MERGE (c:Class {name: $name, file_path: $path}) "
                    "MERGE (f)-[:DEFINES]->(c)",
                    path=file_analysis['file_path'], repo_name=repo_name, name=class_info['name']
                )
                stats['classes'] += 1
                # ... ajouter les méthodes comme relations ...
                
            for func_name in file_analysis['functions']:
                 await session.run(
                    "MATCH (f:File {path: $path, repo_name: $repo_name}) "
                    "MERGE (func:Function {name: $name, file_path: $path}) "
                    "MERGE (f)-[:DEFINES]->(func)",
                    path=file_analysis['file_path'], repo_name=repo_name, name=func_name
                )
                 stats['functions'] += 1
    
    print(f"Graphe peuplé pour le dépôt {repo_name} avec {stats}")
    return stats