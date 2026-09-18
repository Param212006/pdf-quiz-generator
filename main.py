import os
import json
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from groq import Groq

app = FastAPI(title="PDF Quiz Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.get("/")
def read_root():
    return {"status": "online", "message": "PDF Quiz Generator API is running"}

@app.post("/api/generate-quiz")
async def generate_quiz(file: UploadFile = File(...), num_questions: int = Form(20)):
    if not client:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is not set.")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        pdf_bytes = await file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the provided PDF.")

        prompt = f"""
You are an expert educator. Extract key concepts from the following text and generate exactly {num_questions} multiple-choice quiz questions.

CRITICAL INSTRUCTION: Respond ONLY with a raw JSON array. Do not include markdown codeblocks (```json), commentary, or extra text.

JSON format expected:
[
  {{
    "question": "Question string",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Exact matching string from options array",
    "explanation": "Short sentence explaining why this answer is correct"
  }}
]

Text Content:
{extracted_text[:4000]}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content.strip()

        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]

        quiz_data = json.loads(raw_output.strip())
        return {"status": "success", "quiz": quiz_data}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI output into valid JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
