from google import genai
import os

# The new genai SDK automatically looks for the GEMINI_API_KEY environment variable.
try:
    client = genai.Client()
    HAS_LLM = True
except Exception as e:
    print(f"[Brain Warning] LLM initialization failed. Is GEMINI_API_KEY set? Error: {e}")
    HAS_LLM = False

def process_with_llm(user_input, chat_history=""):
    """Generates an AI response using the new google.genai SDK."""
    if not HAS_LLM:
        return "My AI core is offline. Please check your API key configuration."
        
    system_instruction = (
        "You are SPIRIT, an elite, highly sophisticated desktop AI assistant. "
        "Your tone is sharp, intelligent, professional, and slightly futuristic—reminiscent of J.A.R.V.I.S. "
        "Keep your spoken answers concise, direct, and actionable. "
        f"Here is the recent conversation history for context:\n{chat_history}"
    )
    
    full_prompt = f"{system_instruction}\nUser: {user_input}\nSPIRIT:"
    
    try:
        # The new generation syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Quota" in error_msg:
            return "My API rate limit was triggered. Please let the arc reactor cool down for about 10 seconds before your next request."
        return f"Brain connection error: {error_msg}"