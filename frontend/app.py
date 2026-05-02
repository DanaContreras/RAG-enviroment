import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="RAG Local Chat", layout="wide")

st.title("🤖 Chat RAG Local (Gemma 3 + Qdrant)")

# Sidebar para gestión de archivos
with st.sidebar:
    st.header("Documentos")
    uploaded_file = st.file_uploader("Sube un PDF para analizar", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Procesar Documento"):
            with st.spinner("Procesando..."):
                files = {"file": uploaded_file.getvalue()}
                # Usamos el nombre original del archivo
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"Error: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"No se pudo conectar con el backend: {e}")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de chat
if prompt := st.chat_input("¿Qué quieres saber sobre tus documentos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat", 
                    json={"message": prompt}
                )
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    detail = response.json().get('detail', 'Error desconocido')
                    st.error(f"Error del Backend: {detail}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
