# Local RAG System with Gemma 3 & Qdrant

Este proyecto implementa un sistema de Generación Aumentada por Recuperación (RAG) totalmente local utilizando **Gemma 3 (4B)** como modelo de lenguaje, **Qdrant** como base de datos vectorial y **Streamlit** para la interfaz de usuario.

## 🚀 Características

- **LLM Local:** Utiliza Gemma 3 4B a través de Ollama.
- **Embeddings:** `nomic-embed-text` para la vectorización de documentos.
- **Base de Datos Vectorial:** Qdrant para almacenamiento y búsqueda eficiente.
- **Interfaz Web:** Construida con Streamlit para cargar PDFs y chatear con ellos.
- **Orquestación:** Totalmente contenedorizado con Docker Compose.

## 🛠️ Requisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).
- Espacio en disco suficiente para los modelos (~4GB+).

## 📂 Estructura del Proyecto

```text
.
├── backend/            # API FastAPI y lógica de RAG (LangChain)
├── frontend/           # Interfaz Streamlit
├── data/               # Carpeta local para PDFs (sincronizada con el contenedor)
├── docker-compose.yml  # Orquestación de servicios
└── .gitignore          # Archivos ignorados por git
```

## 🚦 Cómo Ejecutar

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd rag_enviroment
   ```

2. **Levantar los servicios:**
   ```bash
   docker-compose up -d
   ```
   *Nota: La primera ejecución tardará unos minutos mientras se descargan las imágenes de Docker y los modelos de Ollama (Gemma 3 y Nomic Embed).*

3. **Acceder a la aplicación:**
   - **Frontend (Interfaz de Chat):** [http://localhost:8501](http://localhost:8501)
   - **Backend (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Qdrant Dashboard:** [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

## 📖 Uso

1. Abre la interfaz de Streamlit en tu navegador.
2. En la barra lateral, sube un archivo **PDF**.
3. Haz clic en **"Procesar Documento"**. Esto dividirá el texto en fragmentos, generará embeddings y los guardará en Qdrant.
4. Escribe tus preguntas en el chat inferior. El sistema recuperará el contexto relevante de tus documentos para generar una respuesta precisa.

## ⚙️ Tecnologías Utilizadas

- **LangChain:** Framework para la orquestación de la cadena RAG.
- **FastAPI:** Framework para el backend.
- **Streamlit:** Framework para el frontend.
- **Ollama:** Servidor local de LLMs.
- **Qdrant:** Vector Database.
