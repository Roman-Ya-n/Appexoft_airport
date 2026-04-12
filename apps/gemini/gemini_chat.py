from google import genai
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = "You are a strict but polite ticket office assistant. Help only with questions about tickets, flights, and payment. If the question is not about flights, say that it is beyond your competence."
def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"