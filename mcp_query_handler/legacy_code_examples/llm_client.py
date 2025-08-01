# core/mcp-servers/query-handler/llm_client.py
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_embedding(text: str, model="text-embedding-3-small") -> list[float]:
    """Génère un embedding pour un texte donné."""
    text = text.replace("\n", " ")
    response = await client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

async def get_completion(user_query: str, context: str, model="gpt-4o") -> str:
    """Génère une réponse à partir d'une requête et d'un contexte."""
    system_prompt = (
        "You are a helpful assistant. Based on the context provided below, "
        "answer the user's query. If the context does not contain the answer, "
        "say that you don't have enough information."
    )
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {user_query}"}
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or "No response from LLM."

