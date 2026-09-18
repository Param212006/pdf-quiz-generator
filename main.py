import os
import json
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pypdf import PdfReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

@app.post("/api/generate-quiz")
async def generate_quiz_api(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    contents = await file.read()
    document_text = extract_text_from_pdf(contents)

    if not document_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is missing.")

    client = Groq(api_key=api_key)

    prompt = f"""
    You are an expert exam setter. Based ONLY on the following text, generate 3 multiple-choice questions.
    Return a valid JSON object with a key "quiz" containing an array of 3 objects.
    Each object must have keys: "question", "options" (array of 4 strings), "answer", and "explanation".

    --- SOURCE TEXT ---
    {document_text[:8000]}
    """

    models_to_try = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama-3.1-8b-instant"
    ]
    last_exception = None

    for model_name in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            raw_output = completion.choices[0].message.content
            parsed = json.loads(raw_output)
            
            if isinstance(parsed, dict):
                quiz_data = parsed.get("quiz") or parsed.get("questions") or list(parsed.values())[0]
            else:
                quiz_data = parsed

            return {"status": "success", "quiz": quiz_data, "model_used": model_name}
        except Exception as e:
            last_exception = e
            print(f"Model {model_name} failed: {e}")
            continue

    raise HTTPException(status_code=500, detail=str(last_exception))
