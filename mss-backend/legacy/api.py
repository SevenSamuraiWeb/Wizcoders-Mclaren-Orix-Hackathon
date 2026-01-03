from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
import uvicorn

# Project Modules
from pdf_processor import PDFProcessor
from vector_store import PageVectorStore
from retriever import ContextRetriever
from credit_memo_generator import CreditMemoGenerator

# Load environment variables
load_dotenv()

# --- Config & Setup ---
app = FastAPI(
    title="Credit Memo Analysis API",
    description="Automated banking credit memo generation using RAG + LLM.",
    version="1.0.0"
)

# CORS (Allow all for prototype)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencies ---
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Groq API Key not configured.")
    return Groq(api_key=api_key)

# --- Models ---
class HealthResponse(BaseModel):
    status: str
    version: str

# --- Endpoints ---
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Simple health check to verify API status.
    """
    return {"status": "ok", "version": "1.0.0"}

@app.post("/analyze")
async def analyze_financial_statement(
    file: UploadFile = File(...),
    client: Groq = Depends(get_groq_client)
):
    """
    Upload a Financial Statement PDF and receive a structured Credit Memo JSON.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    try:
        # 1. Read File
        file_bytes = await file.read()
        
        # 2. Extract Data
        # Using a fresh processor instance per request
        processor = PDFProcessor(file_bytes)
        extracted_data = processor.parse()
        
        if not extracted_data:
            raise HTTPException(status_code=400, detail="Could not extract any content from the PDF.")

        # 3. Build Vector Store
        # Creating a transient store for this request context
        vector_store = PageVectorStore()
        vector_store.add_pages(extracted_data)

        # 4. Context Retrieval & Generation
        retriever = ContextRetriever(vector_store)
        generator = CreditMemoGenerator(
            retriever=retriever, 
            llm_client=client,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct"
        )

        # 5. Generate Memo
        memo = generator.generate_credit_memo()
        
        return memo

    except Exception as e:
        # Log error in production
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
