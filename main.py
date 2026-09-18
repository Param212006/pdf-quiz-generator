import os
import json
import io
import re
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
    return {"status": "online", "message": "PDF Quiz Generator API is live!"}

@app.post("/api/generate-quiz")
async def generate_quiz(file: UploadFile = File(...), num_questions: int = Form(20)):
    if not client:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is not set on Render.")

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

        prompt = f"""You are an educator. Generate exactly {num_questions} multiple-choice questions from this text.
Return ONLY a valid JSON array. No markdown, no triple backticks, no explanatory text.

Format:
[
  {{
    "question": "Question text",
    "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
    "answer": "Opt A",
    "explanation": "Short reason"
  }}
]

Text:
{extracted_text[:2500]}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
        )

        raw_output = response.choices[0].message.content.strip()

        match = re.search(r'\[.*\]', raw_output, re.DOTALL)
        if match:
            clean_json = match.group(0)
            quiz_data = json.loads(clean_json)
            return {"status": "success", "quiz": quiz_data}
        else:
            raise HTTPException(status_code=500, detail="AI output did not contain a valid JSON array.")

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON Parse Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")
