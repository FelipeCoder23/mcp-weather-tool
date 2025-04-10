# =================================================================
# IMPORTACIÓN DE LIBRERÍAS NECESARIAS
# =================================================================
import requests  # Para hacer peticiones HTTP a servicios web
from pydantic import BaseModel, Field  # Para crear modelos de datos validados
from mcp.server.fastmcp import FastMCP  # Framework principal para crear servidor MCP

# =================================================================
# CONFIGURACIÓN DEL SERVIDOR MCP
# =================================================================

# Creamos una instancia del servidor MCP con configuración personalizada
mcp = FastMCP(
    "Servidor del Clima",  # Nombre de nuestro servidor
    instructions="Siempre que te pidan el clima de una ciudad, usa la herramienta 'get_weather'.",  # Instrucciones para el agente
    host="0.0.0.0",  # Acepta conexiones de cualquier IP
    port=8000,  # Puerto donde escuchará el servidor
    debug=False,  # Modo debug desactivado en producción
    log_level="INFO"  # Nivel de detalle en los logs
)

# =================================================================
# MODELO DE DATOS PARA LA RESPUESTA
# =================================================================

# Definimos la estructura de datos que devolverá nuestra API
class WeatherResponse(BaseModel):
    ciudad: str = Field(..., description="Nombre de la ciudad")
    clima: str = Field(..., description="Descripción breve del clima actual")

# =================================================================
# HERRAMIENTA PARA CONSULTAR EL CLIMA
# =================================================================

# Decorador que registra esta función como una herramienta del MCP
@mcp.tool(name="get_weather", description="Obtiene el clima actual de una ciudad")
def get_weather(ciudad: str) -> WeatherResponse:
    """Devuelve el clima actual en formato simple usando wttr.in"""
    # Registramos cada consulta para monitoreo
    print(f"✅ Consultando clima de: {ciudad}")
    
    try:
        # Hacemos la petición a wttr.in, un servicio gratuito de clima
        url = f"https://wttr.in/{ciudad}?format=3"
        response = requests.get(url, timeout=5)  # Timeout de 5 segundos
        resultado = response.text.strip()  # Limpiamos espacios extra
        
        # Devolvemos respuesta en formato estructurado
        return WeatherResponse(ciudad=ciudad, clima=resultado)
    
    except Exception as e:
        # Si algo falla, mostramos el error y devolvemos mensaje amigable
        print(f"❌ Error al obtener clima: {str(e)}")
        return WeatherResponse(ciudad=ciudad, clima="Error al obtener el clima")

# =================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =================================================================

# Solo ejecutamos el servidor si este archivo es el principal
if __name__ == "__main__":
    mcp.run(transport="sse")  # Iniciamos servidor con Server-Sent Events
