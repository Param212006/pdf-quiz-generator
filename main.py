import os
import json
import io
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import pdfplumber
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

# Candidate models ordered by speed and availability
CANDIDATE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768"
]

@app.get("/")
def read_root():
    return {"status": "online", "message": "PDF Quiz Generator API is live!"}

@app.post("/api/generate-quiz")
async def generate_quiz(file: UploadFile = File(...), num_questions: int = Form(20)):
    if not client:
        return {"status": "error", "message": "GROQ_API_KEY is missing on Render."}

    try:
        pdf_bytes = await file.read()
        extracted_text = ""

        # Primary extraction: pypdf
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        except Exception:
            extracted_text = ""

        # Fallback extraction: pdfplumber
        if not extracted_text.strip():
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"

        if not extracted_text.strip():
            return {"status": "error", "message": "Could not extract text from PDF."}

        prompt = f"""Generate exactly {num_questions} multiple-choice questions from this text.
Return ONLY a valid raw JSON array. Do not include markdown codeblocks, commentary, or backticks.

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

        raw_output = None
        last_error = None

        # Sequentially try models until one succeeds
        for model_name in CANDIDATE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=2000
                )
                raw_output = response.choices[0].message.content.strip()
                break
            except Exception as err:
                last_error = err
                continue

        if not raw_output:
            return {"status": "error", "message": f"Groq Error: {str(last_error)}"}

        match = re.search(r'\[.*\]', raw_output, re.DOTALL)
        if match:
            clean_json = match.group(0)
            quiz_data = json.loads(clean_json)
            return {"status": "success", "quiz": quiz_data}
        else:
            return {"status": "error", "message": "AI response formatting error."}

    except Exception as e:
        return {"status": "error", "message": f"Server Error: {str(e)}"}
