# core/shared/schemas/mcp_payload.py
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Literal

# Le type de chunk est littéral pour forcer la standardisation
ChunkType = Literal['text', 'code', 'summary', 'title']

class Chunk(BaseModel):
    """
    Représente un "morceau" de contenu individuel, qu'il s'agisse
    de texte, de code, ou d'un autre type.
    """
    chunk_type: ChunkType = Field(
        ...,
        description="Le type de contenu du chunk."
    )
    content: str = Field(
        ..., 
        description="Le contenu textuel du chunk."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Métadonnées flexibles et spécifiques à la source (URL, nom de fichier, langue du code, etc.)."
    )

    @validator('metadata', pre=True, always=True)
    def ensure_metadata_is_dict(cls, v):
        return v or {}

class SourceInfo(BaseModel):
    """
    Contient les informations sur la source d'où proviennent les chunks.
    """
    source_id: str = Field(
        ...,
        description="Identifiant unique de la source (ex: 'docs.mysite.com', 'project_x_files')."
    )
    summary: str | None = Field(
        None,
        description="Résumé optionnel du contenu de la source, généré par l'IA."
    )
    total_word_count: int = Field(
        0,
        description="Nombre total de mots pour cette source."
    )

class TabularData(BaseModel):
    """
    Représente une collection de données structurées (issues d'un CSV, etc.).
    """
    table_name: str = Field(
        ...,
        description="Nom de la table d'origine (ex: 'ventes_2024.csv')."
    )
    rows: List[Dict[str, Any]] = Field(
        ...,
        description="Liste des lignes de données, chaque ligne étant un dictionnaire."
    )

class MediaReference(BaseModel):
    """
    Représente une référence à un média (image, schéma, etc.) extrait d'un document.
    """
    media_id: str = Field(
        ...,
        description="Identifiant unique du média extrait (ex: nom de fichier, hash)."
    )
    media_type: Literal['image', 'diagram', 'chart', 'other'] = Field(
        'image',
        description="Type du média extrait."
    )
    file_path: str = Field(
        ...,
        description="Chemin relatif ou absolu vers le fichier du média extrait."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Métadonnées additionnelles sur le média (ex: légende, description OCR)."
    )

    @validator('metadata', pre=True, always=True)
    def ensure_metadata_is_dict(cls, v):
        return v or {}

class MCPPayload(BaseModel):
    """
    Le format de payload standardisé que chaque serveur MCP doit retourner.
    C'est le contrat de données principal de la plateforme.
    """
    source_info: SourceInfo = Field(
        ...,
        description="Informations sur la source des données."
    )
    content_chunks: List[Chunk] = Field(
        default_factory=list,
        description="Liste des chunks de contenu textuel ou de code."
    )
    tabular_data: List[TabularData] = Field(
        default_factory=list,
        description="Liste des ensembles de données tabulaires."
    )
    extracted_media_references: List[MediaReference] = Field(
        default_factory=list,
        description="Liste des références aux médias (images, schémas) extraits du document."
    )

    @validator('content_chunks', 'tabular_data', 'extracted_media_references', pre=True, always=True)
    def ensure_lists_are_not_none(cls, v):
        return v or []
