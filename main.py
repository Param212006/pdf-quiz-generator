import os
import json
import io
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import pdfplumber
from groq import Groq

try:
    import dirtyjson
except ImportError:
    dirtyjson = None

app = FastAPI(title="Resume-Based PDF Quiz Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def extract_text_from_pdf_bytes(pdf_bytes):
    extracted_text = ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    except Exception:
        extracted_text = ""

    if not extracted_text.strip():
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
        except Exception:
            extracted_text = ""

    return extracted_text.strip()

def call_groq_llm(prompt):
    if not client:
        raise Exception("GROQ_API_KEY is missing on Render.")

    available_models = []
    try:
        models_response = client.models.list()
        available_models = [m.id for m in models_response.data if "whisper" not in m.id and "safeguard" not in m.id]
    except Exception:
        available_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

    raw_output = None
    last_error = None

    for model_id in available_models:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2500
            )
            raw_output = response.choices[0].message.content.strip()
            if raw_output:
                break
        except Exception as err:
            last_error = err
            continue

    if not raw_output:
        raise Exception(f"Groq API Error: {str(last_error)}")

    return raw_output

def safe_parse_json(json_str):
    clean_str = re.sub(r'```json\s*|\s*```', '', json_str).strip()
    if dirtyjson:
        try:
            return dirtyjson.loads(clean_str)
        except Exception:
            pass
    try:
        return json.loads(clean_str)
    except json.JSONDecodeError:
        fixed_str = re.sub(r',\s*([\]}])', r'\1', clean_str)
        return json.loads(fixed_str)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Resume-Based PDF Quiz Generator API is live!"}

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf_bytes(pdf_bytes)

        if not resume_text:
            return {"status": "error", "message": "Could not extract text from resume PDF."}

        prompt = f"""Analyze this candidate's resume and classify their primary expertise into ONE of these three categories:
1. "Science & Biology" -> recommended_pdf: "sample.pdf"
2. "AI & Machine Learning" -> recommended_pdf: "sample_ai.pdf"
3. "World History & Social Sciences" -> recommended_pdf: "sample_history.pdf"

Return ONLY a valid JSON object.

JSON Format:
{{
  "detected_domain": "AI & Machine Learning",
  "key_skills": ["Python", "FastAPI", "Machine Learning"],
  "recommended_pdf": "sample_ai.pdf",
  "reasoning": "Candidate shows background in software and machine learning."
}}

Resume Content:
{resume_text[:2500]}"""

        raw_response = call_groq_llm(prompt)
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if match:
            analysis = safe_parse_json(match.group(0))
            return {"status": "success", "analysis": analysis}
        else:
            return {"status": "error", "message": "Failed to parse resume analysis response."}

    except Exception as e:
        return {"status": "error", "message": f"Server Error: {str(e)}"}

@app.post("/api/generate-quiz")
async def generate_quiz(file: UploadFile = File(...), num_questions: int = Form(20)):
    try:
        pdf_bytes = await file.read()
        extracted_text = extract_text_from_pdf_bytes(pdf_bytes)

        if not extracted_text:
            return {"status": "error", "message": "Could not extract text from target section PDF."}

        prompt = f"""Generate exactly {num_questions} multiple-choice questions from this text.
Use single quotes inside string values.
Return ONLY raw valid JSON array.

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

        raw_output = call_groq_llm(prompt)
        match = re.search(r'\[.*\]', raw_output, re.DOTALL)
        if match:
            quiz_data = safe_parse_json(match.group(0))
            return {"status": "success", "quiz": quiz_data}
        else:
            return {"status": "error", "message": "AI quiz response formatting error."}

    except Exception as e:
        return {"status": "error", "message": f"Server Error: {str(e)}"}
