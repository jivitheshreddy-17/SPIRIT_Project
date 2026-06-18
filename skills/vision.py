import os
from PIL import Image, ImageGrab
from google import genai
from skills.llm_brain import HAS_LLM

def analyze_screen(command_text=""):
    """Captures the primary monitor and analyzes it using the new google-genai SDK."""
    if not HAS_LLM:
        return "Visual systems are offline. Please verify your Gemini API key."

    # Initialize the modern client
    try:
        client = genai.Client()
    except Exception as e:
        return f"Vision system failed to initialize API client: {e}"

    temp_image_path = "screen_capture.png"
    
    try:
        # Capture the current screen state
        screenshot = ImageGrab.grab()
        screenshot.save(temp_image_path)
        
        # Open the image using PIL for transmission
        img = Image.open(temp_image_path)
        
        prompt = (
            f"You are the visual cortex of SPIRIT. Analyze this screenshot of the user's desktop. "
            f"The user's specific request is: '{command_text}'. "
            "Provide a highly accurate, technical breakdown or answer based strictly on what is visible."
        )
        
        # Use the new SDK multi-modal generation syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt]
        )
        
        # Clean up the local file after processing
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            
        return response.text.strip()
        
    except Exception as e:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        return f"Vision processing error: {str(e)}"