# core/mcp-servers/neo4j-processor/parser.py

from .main import MCPPayload, SourceInfo, Chunk
from . import graph_writer
import git
import tempfile
import os
import ast

def _is_python_file(file_path: str) -> bool:
    return file_path.endswith('.py')

def _analyze_python_file(file_path: str) -> dict:
    """
    Analyse un unique fichier Python avec AST pour en extraire la structure.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    analysis = {
        'classes': [],
        'functions': [],
        'imports': []
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            analysis['classes'].append({'name': node.name, 'methods': []})
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    analysis['classes'][-1]['methods'].append(sub_node.name)
        elif isinstance(node, ast.FunctionDef) and not any(isinstance(p, ast.ClassDef) for p in node.iter_parents()):
             analysis['functions'].append(node.name)
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                analysis['imports'].append(alias.name)
                
    return analysis


async def parse_repository(repo_url: str) -> MCPPayload:
    """
    Orchestre le clonage, l'analyse et la populaton du graphe.
    """
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    print(f"Clonage du dépôt : {repo_url}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        git.Repo.clone_from(repo_url, tmpdir)
        
        all_analysis = []
        file_count = 0
        
        # Parcourir le dépôt cloné
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if _is_python_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        analysis = _analyze_python_file(file_path)
                        analysis['file_path'] = os.path.relpath(file_path, tmpdir)
                        all_analysis.append(analysis)
                        file_count += 1
                    except Exception as e:
                        print(f"Impossible d'analyser le fichier {file_path}: {e}")

        # Écrire les résultats dans le graphe
        stats = await graph_writer.populate_graph_from_analysis(repo_name, all_analysis)
        
    # Créer le payload de synthèse
    source_info = SourceInfo(
        source_id=f"repo_{repo_name}",
        summary=f"Analyse du dépôt {repo_name}. Graphe de connaissances créé."
    )
    
    summary_text = (
        f"Analyse du dépôt terminée.\n"
        f"- Fichiers analysés : {file_count}\n"
        f"- Classes créées : {stats.get('classes', 0)}\n"
        f"- Fonctions créées : {stats.get('functions', 0)}\n"
        f"- Relations créées : {stats.get('relations', 0)}"
    )
    
    summary_chunk = Chunk(
        chunk_type='summary',
        content=summary_text,
        metadata={'repo_url': repo_url}
    )
    
    return MCPPayload(
        source_info=source_info,
        content_chunks=[summary_chunk],
        tabular_data=[]
    )