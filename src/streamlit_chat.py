# =================================================================
# IMPORTACIÓN DE LIBRERÍAS NECESARIAS
# =================================================================
import time  # Para manejar delays y tiempos de espera
import asyncio  # Permite ejecutar código asíncrono (operaciones en paralelo)
import streamlit as st  # Framework para crear aplicaciones web interactivas
from pydantic_ai import Agent  # Clase principal para crear agentes de IA
from pydantic_ai.mcp import MCPServerHTTP  # Cliente para conectar con servidor MCP
from dotenv import load_dotenv  # Carga variables de entorno desde archivo .env
import os  # Funciones para interactuar con el sistema operativo
import traceback  # Herramienta para manejar y mostrar errores detallados

# =================================================================
# CONFIGURACIÓN INICIAL Y VERIFICACIÓN DE API KEY
# =================================================================

# Cargamos las variables de entorno del archivo .env
load_dotenv()

# Verificamos que la clave de OpenAI esté configurada correctamente

if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY no está definido.")
else:
    st.success("🔑 OPENAI_API_KEY cargada correctamente.")

# =================================================================
# CONFIGURACIÓN DEL AGENTE DE IA
# =================================================================

# @st.cache_resource evita que el agente se reinicie cada vez que 
# el usuario interactúa con la app
@st.cache_resource
def setup_agent():
    retries = 5  # Número máximo de intentos de conexión
    for attempt in range(retries):
        try:
            # Creamos conexión con el servidor MCP
            # Usamos el nombre del servicio definido en docker-compose.yml
            mcp_server = MCPServerHTTP(url="http://mcp-server:8000/sse")
            # Inicializamos el agente con GPT-3.5 y nuestro servidor MCP
            return Agent("openai:gpt-3.5-turbo", mcp_servers=[mcp_server])
        except ConnectionError as e:
            # Si falla la conexión, reintentamos hasta 5 veces
            if attempt < retries - 1:
                st.warning(f"Intento {attempt+1} fallido. Reintentando en 3 segundos...")
                time.sleep(3)
            else:
                # Si fallaron todos los intentos, mostramos error
                st.error(f"No se pudo conectar al MCP luego de {retries} intentos: {str(e)}")
                raise
        except Exception as e:
            # Capturamos cualquier otro error inesperado
            st.error(f"❌ Error inesperado al inicializar el agente: {str(e)}")
            raise

# =================================================================
# INICIALIZACIÓN DEL AGENTE CON MANEJO DE ERRORES
# =================================================================

# Intentamos inicializar el agente de forma segura
try:
    agent = setup_agent()
    connection_error = None
except Exception as e:
    agent = None
    connection_error = str(e)

# =================================================================
# INTERFAZ DE USUARIO
# =================================================================

# Configuramos el título principal de nuestra aplicación
st.title("🤖 Chat del Clima (via MCP)")

# Si hubo error de conexión, lo mostramos y detenemos la app
if connection_error:
    st.error("Fallo al iniciar el chatbot. Verifica que el servidor MCP esté activo.")
    st.stop()

# =================================================================
# FUNCIÓN PARA PROCESAR PREGUNTAS DEL USUARIO
# =================================================================

# Función asíncrona que maneja la comunicación con el agente
async def process_query(query):
    try:
        # Ejecutamos los servidores MCP en un contexto asíncrono
        async with agent.run_mcp_servers():
            # Enviamos la pregunta al agente y esperamos respuesta
            result = await agent.run(query)
        return result.data
    except Exception as e:
        # Si hay error, lo mostramos con detalles para debugging
        st.error(f"❌ Error al consultar el agente: {str(e)}")
        st.code(traceback.format_exc(), language="python")
        return None

# =================================================================
# MANEJO DE ENTRADA DEL USUARIO Y RESPUESTAS
# =================================================================

# Campo de texto para que el usuario ingrese su pregunta
user_input = st.text_input("¿Cuál es el clima en...?")

# Cuando el usuario envía una pregunta
if user_input:
    # Mostramos un spinner mientras procesamos la respuesta
    with st.spinner("Consultando el clima..."):
        # Creamos un nuevo loop de eventos para manejar código asíncrono
        # Esto es necesario porque Streamlit no maneja async/await directamente
        loop = asyncio.new_event_loop()
        # Configuramos el loop como el loop principal para este contexto
        asyncio.set_event_loop(loop)
        try:
            # Ejecutamos la consulta y esperamos la respuesta
            # run_until_complete permite ejecutar código asíncrono en un contexto síncrono
            response = loop.run_until_complete(process_query(user_input))
        finally:
            # Siempre cerramos el loop para liberar recursos
            loop.close()

    # Si obtuvimos una respuesta válida, la mostramos
    if response:
        st.markdown(f"**Respuesta:**\n\n{response}")
