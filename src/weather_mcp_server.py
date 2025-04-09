import os
import requests
import logging
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Servidor del Clima",
    instructions="Siempre que te pidan el clima de una ciudad, usa la herramienta 'get_weather'.",
    host="0.0.0.0",
    port=8000,
    debug=False,
    log_level="INFO"
)

class WeatherResponse(BaseModel):
    ciudad: str = Field(..., description="Nombre de la ciudad")
    clima: str = Field(..., description="Descripción breve del clima actual")

@mcp.tool(name="get_weather", description="Obtiene el clima actual de una ciudad")
def get_weather(ciudad: str) -> WeatherResponse:
    """Devuelve el clima actual en formato simple usando wttr.in"""
    logger.info(f"Consultando clima de: {ciudad}")
    try:
        url = f"https://wttr.in/{ciudad}?format=3"
        response = requests.get(url, timeout=5)
        resultado = response.text.strip()
        return WeatherResponse(ciudad=ciudad, clima=resultado)
    except Exception as e:
        logger.error(f"Error al obtener clima: {str(e)}")
        return WeatherResponse(ciudad=ciudad, clima="Error al obtener el clima")

if __name__ == "__main__":
    mcp.run(transport="sse")
