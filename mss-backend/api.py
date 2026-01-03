from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
from fastapi.responses import StreamingResponse
from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from app import generate_word_document

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

class RiskThresholds(BaseModel):
    liquidityRatio: float = 1.0
    debtToEquity: float = 2.5
    netProfitMargin: float = 5.0

class ReportPreferences(BaseModel):
    include5Cs: bool = True
    includeRiskAssessment: bool = True
    includeExecutiveSummary: bool = True

class ApiSettings(BaseModel):
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    apiKey: Optional[str] = None

class UserSettings(BaseModel):
    riskThresholds: RiskThresholds = RiskThresholds()
    reportPreferences: ReportPreferences = ReportPreferences()
    apiSettings: ApiSettings = ApiSettings()

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
    settings: Optional[str] = Form(None),
    client: Groq = Depends(get_groq_client)
):
    """
    Upload a Financial Statement PDF and receive a structured Credit Memo JSON.
    Accepts optional settings for risk thresholds, report preferences, and API config.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    # Parse settings if provided
    user_settings = UserSettings()
    if settings:
        try:
            settings_dict = json.loads(settings)
            user_settings = UserSettings(**settings_dict)
        except Exception as e:
            print(f"Error parsing settings: {e}")
            # Continue with defaults

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

        # 4. Use custom API key if provided
        llm_client = client
        if user_settings.apiSettings.apiKey:
            try:
                llm_client = Groq(api_key=user_settings.apiSettings.apiKey)
            except Exception as e:
                print(f"Error using custom API key: {e}")
                # Fall back to default client

        # 5. Context Retrieval & Generation
        retriever = ContextRetriever(vector_store)
        generator = CreditMemoGenerator(
            retriever=retriever, 
            llm_client=llm_client,
            model_name=user_settings.apiSettings.model,
            settings=user_settings
        )

        # 6. Generate Memo
        memo = generator.generate_credit_memo()
        
        return memo
    except Exception as e:
        # Log error in production
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/download/word")
async def download_word(memo: dict):
    try:
        buffer = generate_word_document(memo)

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": "attachment; filename=credit_memo.docx"
            }
        )

    except Exception as e:
        print("WORD EXPORT ERROR:", e)
        raise HTTPException(status_code=500, detail="Word export failed")



    

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

