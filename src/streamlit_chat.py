import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


print("🔑 Clave API:", os.getenv("OPENAI_API_KEY"))

MCP_URL = "http://localhost:8000/sse"

agent = Agent("openai:gpt-3.5-turbo", mcp_servers=[MCPServerHTTP(url=MCP_URL)])

st.title("🤖 Chat del Clima con MCP")
st.markdown("Pregunta por el clima de una ciudad usando LLM y protocolo MCP.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("¿Cuál es el clima en...?")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Consultando..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(agent.run(prompt))
            response = str(result.data)
        except Exception as e:
            response = f"Error: {str(e)}"
        finally:
            loop.close()
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
