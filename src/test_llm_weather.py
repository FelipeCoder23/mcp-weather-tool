import asyncio
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

load_dotenv()
print("🔑 OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

async def test():
    agent = Agent("openai:gpt-3.5-turbo", mcp_servers=[
        MCPServerHTTP(url="http://127.0.0.1:8000/sse")
    ])
    result = await agent.run("¿Cuál es el clima en Buenos Aires?")
    print("🤖 RESPUESTA DEL AGENTE:")
    print(result.data)

if __name__ == "__main__":
    asyncio.run(test())
