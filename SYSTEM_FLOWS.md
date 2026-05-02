# Flujos del Sistema RAG

Este documento detalla los flujos lógicos del sistema mediante diagramas de secuencia de Mermaid.

## 1. Flujo de Ingesta de Documentos
Este proceso ocurre cuando el usuario sube un PDF desde la interfaz.

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend (app.py)
    participant B as Backend (main.py)
    participant I as Ingestion Service
    participant O as Ollama (nomic-embed)
    participant Q as Qdrant DB

    U->>F: Sube PDF y pulsa "Procesar"
    F->>B: POST /upload (file)
    B->>B: Guarda archivo en data/
    B->>I: process_pdf(file_path)
    I->>I: PyPDFLoader.load()
    I->>I: RecursiveCharacterTextSplitter.split()
    loop Por cada fragmento (chunk)
        I->>O: Generar Embeddings
        O-->>I: Vector
    end
    I->>Q: QdrantVectorStore.from_documents()
    Q-->>I: Confirmación Guardado
    I-->>B: Cantidad de fragmentos
    B-->>F: JSON {message: "Procesado..."}
    F-->>U: Muestra éxito en UI
```

## 2. Flujo de Consulta (RAG Chat)
Este proceso ocurre cuando el usuario realiza una pregunta.

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend (app.py)
    participant B as Backend (main.py)
    participant A as API Service (LangChain)
    participant Q as Qdrant DB
    participant O as Ollama (Gemma 3)

    U->>F: Escribe pregunta
    F->>B: POST /chat {message}
    B->>A: get_rag_chain()
    A->>Q: Búsqueda de similitud (retriever)
    Q-->>A: Retorna Chunks relevantes
    A->>A: Construye Prompt (Contexto + Pregunta)
    A->>O: ChatOllama.invoke(prompt)
    O-->>A: Genera Respuesta (String)
    A-->>B: Respuesta final
    B-->>F: JSON {response: "..."}
    F-->>U: Muestra respuesta en el chat
```

## 📂 Archivos Clave para el Entendimiento

| Archivo | Responsabilidad |
| :--- | :--- |
| `docker-compose.yml` | Orquestación de servicios (Ollama, Qdrant, Backend, Frontend). |
| `frontend/app.py` | Interfaz de usuario con Streamlit y llamadas a la API. |
| `backend/main.py` | Definición de endpoints FastAPI y manejo de archivos. |
| `backend/services/ingestion.py` | Lógica de extracción de texto, fragmentación y carga en Qdrant. |
| `backend/services/api.py` | Configuración de la cadena RAG con LangChain y Gemma 3. |
| `.gitignore` | Configuración para evitar subir datos locales o binarios. |
