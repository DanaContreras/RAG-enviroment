import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
COLLECTION_NAME = "pdf_documents"

def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_BASE_URL
    )

def process_pdf(file_path: str):
    # 1. Cargar el PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2. Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Inicializar Embeddings
    embeddings = get_embeddings()

    # 4. Guardar en Qdrant usando el método estático pero con los nombres de parámetros verificados
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=f"http://{QDRANT_HOST}:6333",
        collection_name=COLLECTION_NAME,
        force_recreate=False
    )
    
    return len(chunks)

def get_vector_store():
    embeddings = get_embeddings()
    
    # Intentamos conectar directamente
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        url=f"http://{QDRANT_HOST}:6333"
    )
