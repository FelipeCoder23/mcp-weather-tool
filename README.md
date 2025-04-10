# MCP Weather Chat
Una aplicación de chat del clima que utiliza MCP (Modular Capability Protocol) y GPT-3.5 para proporcionar información meteorológica en lenguaje natural.

## Descripción General
MCP Weather Chat es una aplicación containerizada que demuestra el uso del Protocolo de Capacidad Modular (MCP) para permitir que un modelo de lenguaje (LLM) interactúe con servicios externos. Esta implementación incluye un servidor del clima que utiliza wttr.in y una interfaz frontend construida con Streamlit.

## Características
- **Arquitectura Containerizada**: Contenedores separados para el servidor MCP y la aplicación cliente
- **Integración con wttr.in**: Datos del clima en tiempo real usando el servicio gratuito wttr.in
- **Interfaz Streamlit**: UI limpia y responsiva para interactuar con el chat
- **Comunicación SSE**: Server-Sent Events para comunicación en tiempo real
- **Integración GPT-3.5**: Potenciado por el modelo GPT-3.5 de OpenAI para entender lenguaje natural

## Arquitectura
La aplicación consta de dos componentes principales:
- **MCP Server**: Servicio basado en FastMCP que maneja la obtención de datos del clima
- **Streamlit Client**: Interfaz web para interactuar con el chatbot

## Empezando

### Prerrequisitos
- Docker y Docker Compose
- OpenAI API Key (registrarse en OpenAI)

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/mcp-weather-chat.git
cd mcp-weather-chat
```

2. Crear archivo .env:
```bash
OPENAI_API_KEY=tu_api_key_de_openai_aqui
```

3. Iniciar la aplicación:
```bash
docker-compose up --build
```

4. Acceder a la interfaz:
- Abrir navegador en: http://localhost:8510

## Uso
Una vez que la aplicación esté corriendo, puedes interactuar con el chatbot a través de la interfaz Streamlit:

Ejemplos de preguntas:
- "¿Cuál es el clima en Madrid?"
- "¿Qué tiempo hace en Tokyo?"
- "¿Cómo está el clima en Buenos Aires?"

## Estructura del Proyecto
```
mcp-weather-chat/
├── .env                    # Variables de entorno
├── docker-compose.yml      # Configuración de Docker Compose
├── Dockerfile.server       # Dockerfile para servidor MCP
├── Dockerfile.streamlit    # Dockerfile para cliente Streamlit
├── README.md              # Documentación del proyecto
└── src/                   # Código fuente
    ├── weather_mcp_server.py  # Implementación del servidor del clima
    └── streamlit_chat.py      # Aplicación cliente Streamlit
```

## Stack Tecnológico
- **FastMCP**: Framework para crear servidores MCP
- **Streamlit**: Framework web para la UI
- **Pydantic**: Validación de datos y modelos
- **Docker**: Plataforma de containerización
- **OpenAI GPT-3.5**: LLM para procesamiento de lenguaje natural
- **wttr.in**: Servicio de datos meteorológicos

## Solución de Problemas

### Problemas Comunes
- **Error de Conexión**: Asegúrate de que todos los servicios estén funcionando. El cliente tiene un mecanismo de reintento.
- **Errores de API Key**: Verifica que hayas agregado una API key válida de OpenAI en el archivo .env.
- **Problemas de Red Docker**: Si los contenedores no pueden comunicarse, verifica la configuración de red en docker-compose.yml.

## Puertos
- **Servidor MCP**: 8010
- **Cliente Streamlit**: 8510

## Gracias por ver mi contenido :D 