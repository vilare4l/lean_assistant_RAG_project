# core/mcp-servers/media-processor/clients.py

import os
import openai
import base64

# Configurer le client OpenAI (la clé est chargée depuis les variables d'env)
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_image_description(asset_url: str, image_content: bytes) -> str:
    """
    Génère une description pour une image en utilisant l'API Vision d'OpenAI.
    """
    if not openai.api_key:
        raise ValueError("La clé API OpenAI n'est pas configurée.")

    # Encoder l'image en base64
    base64_image = base64.b64encode(image_content).decode('utf-8')

    try:
        response = await openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Décris cette image en détail. Si elle contient du texte (OCR), extrais-le également."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API Vision d'OpenAI : {e}")
        return f"Impossible de générer une description pour l'image à l'URL : {asset_url}"


async def get_audio_transcription(asset_url: str, audio_content: bytes) -> str:
    """
    Génère une transcription pour un fichier audio en utilisant l'API Whisper d'OpenAI.
    """
    if not openai.api_key:
        raise ValueError("La clé API OpenAI n'est pas configurée.")

    try:
        # Note: L'API Whisper de la bibliothèque openai ne supporte pas directement les bytes en async.
        # Une implémentation de production utiliserait `aiohttp` pour streamer le fichier.
        # Pour ce MVP, nous utilisons une approche simple qui peut être moins performante.
        
        # Il faut sauvegarder temporairement le fichier pour que l'API puisse le lire.
        temp_file_path = "/tmp/temp_audio_file"
        with open(temp_file_path, "wb") as f:
            f.write(audio_content)

        with open(temp_file_path, "rb") as audio_file:
            transcription = await openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        os.remove(temp_file_path)
        
        return transcription.text
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API Whisper d'OpenAI : {e}")
        return f"Impossible de générer une transcription pour l'audio à l'URL : {asset_url}"