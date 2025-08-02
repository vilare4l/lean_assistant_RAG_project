# core/mcp-servers/web-crawler/processor.py

import asyncio
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

# Schémas Pydantic (supposés être dans main.py pour l'instant)
from .main import MCPPayload, SourceInfo, Chunk

# Fonctions utilitaires
from .utils import (
    smart_chunk_markdown,
    extract_code_blocks,
    process_code_blocks_in_parallel,
    extract_source_summary,
    extract_section_info
)

async def process_url(url: str) -> MCPPayload:
    """
    Orchestre le crawling d'une URL et sa transformation en MCPPayload.
    """
    
    # 1. Initialiser et exécuter le crawler
    crawler = AsyncWebCrawler()
    async with crawler:
        run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=False)
        result = await crawler.arun(url=url, config=run_config)

    if not result or not result.success or not result.markdown:
        raise RuntimeError(f"Failed to crawl URL: {url}. Error: {result.error_message if result else 'Unknown'}")

    markdown_content = result.markdown
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path

    # 2. Extraire le résumé de la source
    source_summary = extract_source_summary(domain, markdown_content)
    
    all_chunks: list[Chunk] = []
    total_word_count = 0

    # 3. Traiter et chunker le contenu textuel
    text_chunks_content = smart_chunk_markdown(markdown_content)
    for chunk_content in text_chunks_content:
        meta_info = extract_section_info(chunk_content)
        total_word_count += meta_info.get("word_count", 0)
        
        all_chunks.append(Chunk(
            chunk_type='text',
            content=chunk_content,
            metadata={
                'url': url,
                'headers': meta_info.get('headers', ''),
                'char_count': meta_info.get('char_count', 0)
            }
        ))

    # 4. Extraire et traiter les blocs de code
    code_blocks = extract_code_blocks(markdown_content)
    if code_blocks:
        # Générer les résumés pour les blocs de code en parallèle
        processed_code_blocks = process_code_blocks_in_parallel(code_blocks)
        
        for block in processed_code_blocks:
            total_word_count += len(block['code'].split())
            all_chunks.append(Chunk(
                chunk_type='code',
                content=block['code'],
                metadata={
                    'url': url,
                    'language': block['language'],
                    'summary': block.get('summary', 'N/A')
                }
            ))

    # 5. Assembler le payload final
    source_info = SourceInfo(
        source_id=domain,
        summary=source_summary,
        total_word_count=total_word_count
    )
    
    payload = MCPPayload(
        source_info=source_info,
        content_chunks=all_chunks,
        tabular_data=[]
    )
    
    return payload