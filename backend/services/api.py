import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .ingestion import get_vector_store

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

def get_rag_chain():
    # 1. Configurar LLM
    llm = ChatOllama(
        model="gemma3:4b",
        base_url=OLLAMA_BASE_URL
    )

    # 2. Configurar Retriever
    try:
        vectorstore = get_vector_store()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        print(f"Error cargando vectorstore: {e}")
        raise e

    # 3. Definir Prompt
    template = """Responde a la pregunta basándote únicamente en el siguiente contexto:
    {context}

    Pregunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 4. Construir cadena LCEL
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
