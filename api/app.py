# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import shutil
from typing import Optional, List
import uuid

# Import Pydantic for data validation and settings management
from pydantic import BaseModel

# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI

# Import aimakerspace components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aimakerspace.text_utils import PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.embedding import EmbeddingModel as BaseEmbeddingModel

# Custom EmbeddingModel that accepts API key as parameter
class EmbeddingModel(BaseEmbeddingModel):
    def __init__(self, api_key: str, embeddings_model_name: str = "text-embedding-3-small"):
        from openai import AsyncOpenAI, OpenAI
        import openai
        
        # Store the API key
        self.openai_api_key = api_key
        self.embeddings_model_name = embeddings_model_name
        
        # Initialize clients with the provided API key
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.client = OpenAI(api_key=api_key)
        
        # Set the global API key for compatibility
        openai.api_key = api_key

# Initialize FastAPI application with a title
app = FastAPI(title="PDF RAG Chat API")

# Configure CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Global storage for vector databases (in production, use a proper database)
vector_databases = {}

# Define the data models using Pydantic
class ChatRequest(BaseModel):
    user_message: str
    pdf_id: str
    model: Optional[str] = "gpt-4o-mini"
    api_key: str

    class Config:
        # Allow extra fields and be more flexible
        extra = "allow"
        validate_assignment = False

class UploadResponse(BaseModel):
    pdf_id: str
    message: str
    chunks_count: int

    class Config:
        extra = "allow"

class PDFListResponse(BaseModel):
    pdfs: List[dict]

    class Config:
        extra = "allow"

# Helper function to create a unique PDF ID
def create_pdf_id() -> str:
    return str(uuid.uuid4())

# Helper function to get PDF path by ID
def get_pdf_path(pdf_id: str) -> str:
    return os.path.join(UPLOADS_DIR, f"{pdf_id}.pdf")

# Helper function to process and index PDF
async def process_pdf(pdf_path: str, pdf_id: str, api_key: str) -> int:
    """Process PDF and create vector database index"""
    try:
        print(f"=== PROCESS_PDF DEBUG ===")
        print(f"Processing PDF: {pdf_path}")
        print(f"PDF exists: {os.path.exists(pdf_path)}")
        print(f"PDF size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 'N/A'} bytes")
        
        # Load PDF content
        print("Creating PDFLoader...")
        pdf_loader = PDFLoader(pdf_path)
        print("PDFLoader created successfully")
        
        print("Loading documents...")
        documents = pdf_loader.load_documents()
        print(f"Documents loaded: {len(documents)}")
        print(f"First document length: {len(documents[0]) if documents else 0}")
        
        if not documents:
            raise ValueError("No text content found in PDF")
        
        # Split text into chunks
        print("Creating text splitter...")
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        print("Text splitter created successfully")
        
        print("Splitting text into chunks...")
        chunks = splitter.split_texts(documents)
        print(f"Text split into {len(chunks)} chunks")
        print(f"First chunk length: {len(chunks[0]) if chunks else 0}")
        
        # Create vector database with API key
        print("Creating EmbeddingModel...")
        embedding_model = EmbeddingModel(api_key=api_key)
        print("EmbeddingModel created successfully")
        
        print("Creating VectorDatabase...")
        vector_db = VectorDatabase(embedding_model)
        print("VectorDatabase created successfully")
        
        # Build vector database from chunks
        print("Building vector database from chunks...")
        await vector_db.abuild_from_list(chunks)
        print("Vector database built successfully")
        
        # Store vector database
        print("Storing vector database...")
        vector_databases[pdf_id] = {
            'vector_db': vector_db,
            'chunks': chunks,
            'chunk_count': len(chunks)
        }
        print(f"Vector database stored for PDF ID: {pdf_id}")
        print("=== PROCESS_PDF COMPLETED ===")
        
        return len(chunks)
        
    except Exception as e:
        print(f"=== PROCESS_PDF ERROR ===")
        print(f"Error in process_pdf: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error args: {e.args}")
        import traceback
        traceback.print_exc()
        print("=== END PROCESS_PDF ERROR ===")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Upload PDF endpoint
@app.post("/api/upload-pdf", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    api_key: str = Form(...)
):
    """Upload and index a PDF file"""
    try:
        print(f"Starting upload process...")
        print(f"File name: {file.filename}")
        print(f"API key starts with sk-: {api_key.startswith('sk-')}")
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate API key format (basic check)
        if not api_key.startswith('sk-'):
            raise HTTPException(status_code=400, detail="Invalid OpenAI API key format")
        
        print("File and API key validation passed")
        
        # Create unique PDF ID
        pdf_id = create_pdf_id()
        pdf_path = get_pdf_path(pdf_id)
        print(f"PDF ID: {pdf_id}")
        print(f"PDF Path: {pdf_path}")
        
        # Save uploaded file
        print("Saving uploaded file...")
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("File saved successfully")
        
        # Process and index the PDF
        print("Starting PDF processing...")
        chunks_count = await process_pdf(pdf_path, pdf_id, api_key)
        print(f"PDF processing completed. Chunks: {chunks_count}")
        
        return UploadResponse(
            pdf_id=pdf_id,
            message=f"PDF uploaded and indexed successfully",
            chunks_count=chunks_count
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        print("HTTPException caught and re-raising")
        raise
    except Exception as e:
        # Log the full error for debugging
        print(f"Upload error: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error args: {e.args}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# List uploaded PDFs endpoint
@app.get("/api/pdfs", response_model=PDFListResponse)
async def list_pdfs():
    """List all uploaded and indexed PDFs"""
    pdfs = []
    for pdf_id, data in vector_databases.items():
        pdf_path = get_pdf_path(pdf_id)
        if os.path.exists(pdf_path):
            pdfs.append({
                "id": pdf_id,
                "filename": f"{pdf_id}.pdf",
                "chunks_count": data['chunk_count']
            })
    
    return PDFListResponse(pdfs=pdfs)

# RAG Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with the uploaded PDF using RAG"""
    try:
        # Check if PDF exists and is indexed
        if request.pdf_id not in vector_databases:
            raise HTTPException(status_code=404, detail="PDF not found or not indexed")
        
        # Get vector database and chunks
        pdf_data = vector_databases[request.pdf_id]
        vector_db = pdf_data['vector_db']
        chunks = pdf_data['chunks']
        
        # Search for relevant chunks
        relevant_chunks = vector_db.search_by_text(
            request.user_message, 
            k=3, 
            return_as_text=True
        )
        
        # Create context from relevant chunks
        context = "\n\n".join(relevant_chunks)
        
        # Initialize OpenAI client
        client = OpenAI(api_key=request.api_key)
        
        # Create system prompt for RAG
        system_prompt = f"""You are a helpful assistant that answers questions based on the provided context from a PDF document. 
        
        Context from the PDF:
        {context}
        
        Please answer the user's question based on the context provided. If the answer cannot be found in the context, say so clearly. 
        Always cite specific parts of the context when possible."""
        
        # Create async generator for streaming response
        async def generate():
            try:
                stream = client.chat.completions.create(
                    model=request.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": request.user_message}
                    ],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
                        
            except Exception as e:
                yield f"Error: {str(e)}"
        
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete PDF endpoint
@app.delete("/api/pdfs/{pdf_id}")
async def delete_pdf(pdf_id: str):
    """Delete a PDF and its index"""
    try:
        # Remove from vector databases
        if pdf_id in vector_databases:
            del vector_databases[pdf_id]
        
        # Remove file
        pdf_path = get_pdf_path(pdf_id)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        return {"message": "PDF deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "indexed_pdfs": len(vector_databases)}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
