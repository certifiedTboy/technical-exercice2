import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"




app = FastAPI(title="AI Text Summarizer Interview")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"]
)

# TODO 0:
# Initialize the Ollama language model using llama3.2:3b
# and configure the temperature .


# model = os.getenv("AI-MODEL")

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0    
)

class SummaryRequest(BaseModel):
    text: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/summarize")
def summarize(data: SummaryRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # TODO 1: Create a prompt asking the AI to summarize data.text
    prompt = [("system", 
               """
                You are a helpful assistant that summarizes users text"
               1. Your primary role is to summarize the text into 2 sentence
               2. If you user request for an service that is different from you primary role, creatively reply them and remind them of your primary role 
               """
    ),

    ("human", {data.text})
    ]

    # TODO 2: Send the prompt to Ollama 
    # Extract the generated text from the response.
    summary = llm.invoke(prompt)

    if summary is None:
        raise HTTPException(
            status_code=501,
            detail="Complete TODO 1 and TODO 2 in app.py",
        )

    # TODO 3: Return the summary as JSON
    return { "status" : "success", "result": summary }


# Keep the frontend mount after the API routes.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    print("Open http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
