import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# LLM ANSWER FUNCTION
# -----------------------------
def ask_llm(question, context_chunks):

    try:

        if not context_chunks:
            return "Not found in provided data."

        # Limit context size (VERY IMPORTANT for mobile + API stability)
        context = "\n\n".join(context_chunks[:8])

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the provided context to answer.

If the answer is not in the context, respond:
"Not found in provided data."

CONTEXT:
{context}

QUESTION:
{question}
"""

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"