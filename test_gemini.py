
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    print("ERROR: API key not found in .env")

else:
    try:
        print("Connecting to Gemini...")

        with genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=120000)
        ) as client:

            response = client.models.generate_content(
                model=model_name,
                contents="Reply with only: Gemini connection successful."
            )

            print("\nSUCCESS!")
            print(response.text)

    except Exception as e:
        print("\nGemini error:", repr(e))
