# core/mcp-servers/web-crawler/utils.py

import os
import re
import time
import openai
import concurrent.futures
from typing import List, Dict, Any

# --- Fonctions de traitement de texte et de code ---

def smart_chunk_markdown(text: str, chunk_size: int = 5000) -> List[str]:
    """Split text into chunks, respecting code blocks and paragraphs."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        if end >= text_length:
            chunks.append(text[start:].strip())
            break

        chunk_view = text[start:end]
        
        # Priorité aux blocs de code
        code_block_end = chunk_view.rfind('```')
        if code_block_end > chunk_size * 0.3:
            end = start + code_block_end
        # Ensuite les paragraphes
        elif '\n\n' in chunk_view:
            last_break = chunk_view.rfind('\n\n')
            if last_break > chunk_size * 0.3:
                end = start + last_break
        # Enfin les phrases
        elif '. ' in chunk_view:
            last_period = chunk_view.rfind('. ')
            if last_period > chunk_size * 0.3:
                end = start + last_period + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks

def extract_section_info(chunk: str) -> Dict[str, Any]:
    """Extracts headers and stats from a chunk."""
    headers = re.findall(r'^(#+)\s+(.+)$', chunk, re.MULTILINE)
    header_str = '; '.join([f'{h[0]} {h[1]}' for h in headers]) if headers else ''
    return {
        "headers": header_str,
        "char_count": len(chunk),
        "word_count": len(chunk.split())
    }

def extract_code_blocks(markdown_content: str, min_length: int = 100) -> List[Dict[str, Any]]:
    """Extract code blocks from markdown content along with context."""
    code_blocks = []
    # Regex pour trouver les blocs de code avec leur langage optionnel
    pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
    matches = pattern.finditer(markdown_content)

    for match in matches:
        language = match.group(1).strip()
        code_content = match.group(2).strip()

        if len(code_content) < min_length:
            continue

        code_blocks.append({
            'code': code_content,
            'language': language if language else 'unknown',
        })
    return code_blocks

# --- Fonctions d'interaction avec l'IA (pour les résumés) ---

def generate_summary_with_llm(prompt: str, model_choice: str) -> str:
    """Fonction générique pour appeler un LLM pour un résumé."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model=model_choice,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides concise summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary with LLM: {e}")
        return ""

def generate_code_example_summary(code: str) -> str:
    """Generate a summary for a code example."""
    model_choice = os.getenv("MODEL_CHOICE", "gpt-3.5-turbo")
    prompt = f"""
<code_example>
{code[:2000]}
</code_example>

Based on the code example, provide a concise summary (2-3 sentences) that describes what this code example demonstrates and its purpose. Focus on the practical application and key concepts illustrated.
"""
    return generate_summary_with_llm(prompt, model_choice)

def extract_source_summary(source_id: str, content: str) -> str:
    """Extract a summary for a source from its content."""
    model_choice = os.getenv("MODEL_CHOICE", "gpt-3.5-turbo")
    prompt = f"""
<source_content>
{content[:4000]}
</source_content>

The above content is from the documentation for '{source_id}'. Please provide a concise summary (3-5 sentences) that describes what this library/tool/framework is about.
"""
    return generate_summary_with_llm(prompt, model_choice)

def process_code_blocks_in_parallel(code_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes a list of code blocks in parallel to add summaries.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Crée un future pour chaque résumé à générer
        future_to_block = {executor.submit(generate_code_example_summary, block['code']): block for block in code_blocks}
        
        for future in concurrent.futures.as_completed(future_to_block):
            block = future_to_block[future]
            try:
                summary = future.result()
                block['summary'] = summary
            except Exception as exc:
                print(f"Block {block['code'][:30]}... generated an exception: {exc}")
                block['summary'] = "Could not generate summary."
    return code_blocks

