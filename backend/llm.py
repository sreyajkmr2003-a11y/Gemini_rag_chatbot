import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(question, context_chunks):
    try:
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not in the context, say:
"Not found in provided data."

CONTEXT:
{context}

QUESTION:
{question}
"""

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"