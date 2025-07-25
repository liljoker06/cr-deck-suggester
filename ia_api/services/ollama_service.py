import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

async def query_llm(prompt: str, model: str = "llama3.1:8b") -> str:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "⚠️ Réponse vide.")
    except Exception as e:
        print(f"❌ Erreur dans query_llm: {e}")
        return f"❌ Erreur : {str(e)}"
