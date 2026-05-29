import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ingestion import process_pdf
from services.api import get_rag_chain

app = FastAPI()

# Configuración de CORS para Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    message: str
    provider: str = "ollama"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks_count = process_pdf(file_path)
        return {"message": f"Archivo {file.filename} procesado exitosamente en {chunks_count} fragmentos."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files():
    try:
        files = os.listdir(DATA_DIR)
        return {"files": [f for f in files if f.endswith(".pdf")]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        chain = get_rag_chain(provider=request.provider)
        response = chain.invoke(request.message)
        return {"response": response}
    except Exception as e:
        print(f"ERROR EN CHAT: {str(e)}") # Esto aparecerá en tus logs de docker
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
