import requests
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Servidor del Clima",
    instructions="Siempre que te pidan el clima de una ciudad, usa la herramienta 'get_weather'.",
    host="0.0.0.0",
    port=8000
)

@mcp.tool(name="get_weather", description="Obtiene el clima actual de una ciudad")
def get_weather(ciudad: str) -> str:
    """Devuelve el clima actual en formato simple."""
    logger.info(f"get_weather(ciudad='{ciudad}')")
    try:
        url = f"https://wttr.in/{ciudad}?format=3"
        response = requests.get(url, timeout=5)
        resultado = response.text.strip()
        logger.info(f"get_weather() -> {resultado}")
        return resultado
    except Exception as e:
        error = f"Error al obtener el clima: {str(e)}"
        logger.error(error)
        return error

if __name__ == "__main__":
    
    mcp.run(transport="sse")
