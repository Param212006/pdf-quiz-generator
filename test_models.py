import os
from google import genai

client = genai.Client()

models_to_test = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']

for m in models_to_test:
    try:
        res = client.models.generate_content(model=m, contents="Say hello")
        print(f"SUCCESS: '{m}' works! Response: {res.text.strip()}")
        break
    except Exception as e:
        print(f"FAILED: '{m}' -> {e}")
