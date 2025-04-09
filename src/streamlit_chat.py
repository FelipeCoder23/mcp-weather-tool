import time
import asyncio
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from dotenv import load_dotenv
import os
import traceback

# Cargar variables de entorno
load_dotenv()

# Asegurar que la clave API está presente
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY no está definido.")
else:
    st.success("🔑 OPENAI_API_KEY cargada correctamente.")

# 🧠 Setup del agente con cache + reintentos
@st.cache_resource
def setup_agent():
    retries = 5
    for attempt in range(retries):
        try:
            # Conectamos usando el nombre del servicio definido en docker-compose.yml
            mcp_server = MCPServerHTTP(url="http://mcp-server:8000/sse")
            return Agent("openai:gpt-3.5-turbo", mcp_servers=[mcp_server])
        except ConnectionError as e:
            if attempt < retries - 1:
                st.warning(f"Intento {attempt+1} fallido. Reintentando en 3 segundos...")
                time.sleep(3)
            else:
                st.error(f"No se pudo conectar al MCP luego de {retries} intentos: {str(e)}")
                raise
        except Exception as e:
            st.error(f"❌ Error inesperado al inicializar el agente: {str(e)}")
            raise

# Inicializar agente con control de errores
try:
    agent = setup_agent()
    connection_error = None
except Exception as e:
    agent = None
    connection_error = str(e)

# Título de la app
st.title("🤖 Chat del Clima (via MCP)")

# Mostrar error si falló la conexión
if connection_error:
    st.error("Fallo al iniciar el chatbot. Verifica que el servidor MCP esté activo.")
    st.stop()

# Función para procesar preguntas
async def process_query(query):
    try:
        async with agent.run_mcp_servers():
            result = await agent.run(query)
        return result.data
    except Exception as e:
        st.error(f"❌ Error al consultar el agente: {str(e)}")
        st.code(traceback.format_exc(), language="python")
        return None

# Input del usuario
user_input = st.text_input("¿Cuál es el clima en...?")

# Procesar respuesta
if user_input:
    with st.spinner("Consultando el clima..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(process_query(user_input))
        finally:
            loop.close()

    if response:
        st.markdown(f"**Respuesta:**\n\n{response}")
