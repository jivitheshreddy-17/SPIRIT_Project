import speech_recognition as sr
import pyttsx3
import sys
import time
import os
from groq import Groq
import re

# --- SKILL IMPORTS ---
from skills.audio_control import adjust_volume
from skills.workspace import organize_folder
from skills.os_operator import launch_app, close_app, minimize_all_windows
from skills.vitals import get_system_status, adjust_brightness, set_power_plan
from skills.vision import analyze_screen
from skills.file_manager import take_note, manage_files
from skills.system_monitor import start_pomodoro
from skills.web_search import perform_web_search
from skills.llm_brain import process_with_llm, HAS_LLM
from skills.terminal_ui import display_system_boot, display_user_input, display_agent_response, display_standby

# Global memory storage for basic turn tracking
chat_history = ""

# Initialize Groq for flawless Speech-to-Text
try:
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    HAS_GROQ = True if os.environ.get("GROQ_API_KEY") else False
except Exception as e:
    print(f"[Warning] Groq initialization failed. Check GROQ_API_KEY. {e}")
    HAS_GROQ = False

def speak(vocal_text, display_text=None):
    """Handles dual-channel processing with a fresh audio thread to prevent SAPI5 crashes."""
    if display_text:
        display_agent_response(display_text)
    else:
        display_agent_response(vocal_text)
        
    try:
        # Spin up a fresh engine for every speech event to prevent background thread lockups
        local_engine = pyttsx3.init()
        voices = local_engine.getProperty('voices')
        local_engine.setProperty('voice', voices[0].id) 
        local_engine.setProperty('rate', 185)           
        local_engine.say(vocal_text)
        local_engine.runAndWait()
    except Exception as e:
        print(f"\n[Audio Error: System muted. {e}]")

def transcribe_with_groq(audio_data):
    """Transcribes audio completely in-memory via Groq Whisper, bypassing the hard drive."""
    if not HAS_GROQ:
        # Fallback to the old Google API if Groq isn't configured
        recognizer = sr.Recognizer()
        try:
            return recognizer.recognize_google(audio_data, language='en-in').lower()
        except Exception:
            return ""

    try:
        # Extract the raw WAV bytes directly from RAM
        wav_bytes = audio_data.get_wav_data()
        
        # Send the bytes directly to Groq without creating a physical file
        transcription = groq_client.audio.transcriptions.create(
            file=("memory_audio.wav", wav_bytes),
            model="whisper-large-v3",
            response_format="text",
            language="en"
        )
        
        # Strip all punctuation (periods, commas, etc.) using regex
        clean_text = re.sub(r'[^\w\s]', '', transcription)
        return clean_text.strip().lower()
        
    except Exception as e:
        print(f"[Whisper Error: {e}]")
        return ""
def listen_for_wake_word():
    """Passive listener with locked sensitivity for instant triggering via Groq Whisper."""
    recognizer = sr.Recognizer()
    
    # Turn off dynamic volume adjustment to prevent "deafness"
    recognizer.dynamic_energy_threshold = False 
    recognizer.energy_threshold = 400  # Static sensitivity (Lower = more sensitive)
    recognizer.pause_threshold = 0.5  
    
    with sr.Microphone() as source:
        display_standby()
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=8)
            return transcribe_with_groq(audio)
        except sr.WaitTimeoutError:
            return ""
        except Exception:
            return ""

def listen_command():
    """Active listener capturing your full command for Groq Whisper execution."""
    recognizer = sr.Recognizer()
    
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 400
    recognizer.pause_threshold = 2.0  

    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=20)
            command = transcribe_with_groq(audio)
            if command:
                display_user_input(command)
            return command
        except sr.WaitTimeoutError:
            speak("Session timeout due to inactivity.")
            return ""
        except Exception:
            speak("Audio signal unclear. Please repeat.")
            return ""

def execute_skill(command):
    """Central processing pipeline to execute hardcoded tools or send to LLM."""
    global chat_history
    
    # --- PHASE 1: HARD CODED CRITICAL AUTOMATIONS ---
    if any(word in command for word in ["goodbye", "exit", "quit", "stop"]):
        speak("Powering down arc reactor. Goodbye.")
        sys.exit()

    # --- PHASE 1.9: WORKSPACE ORGANIZER (High Priority Routing) ---
    elif any(phrase in command for phrase in ["clean up folder", "organize folder", "clean my downloads"]):
        speak("Analyzing directory layout...")
        target_directory = r"C:\Users\jivit\Documents\SPIRIT_Project"
        
        if "downloads" in command:
            target_directory = os.path.expanduser("~/Downloads")
            
        result = organize_folder(target_directory)
        speak(result)
        
    elif any(phrase in command for phrase in ["note down", "take a note", "save note", "record this"]):
        response = take_note(command)
        speak(response)
        
    elif any(word in command for word in ["create", "delete", "remove", "clean", "clear"]):
        response = manage_files(command)
        speak(response)
        
    elif any(word in command for word in ["timer", "study", "session", "focus", "time"]):
        response = start_pomodoro(command)
        speak(response)
        
    # --- PHASE 1.5: MULTIMODAL VISION ---
    elif any(phrase in command for phrase in ["look at my screen", "what is on my screen", "read my screen", "analyze my screen"]):
        speak("Accessing optical data. Scanning screen...")
        response = analyze_screen(command)
        
        if "```" in response or len(response) > 200:
            short_speech = "Screen analysis complete. I have output the detailed breakdown to your terminal."
            speak(short_speech, display_text=response)
        else:
            speak(response)
            
    # --- PHASE 1.7: HARDWARE VITALS & CONTROL ---
    elif any(phrase in command for phrase in ["status", "vitals", "battery", "cpu", "ram"]):
        speak("Running system diagnostics...")
        report = get_system_status()
        speak(report)
        
    elif "brightness" in command:
        response = adjust_brightness(command)
        speak(response)
        
    elif "volume" in command or "mute" in command:
        response = adjust_volume(command)
        speak(response)
        
    elif "power plan" in command or "performance mode" in command:
        response = set_power_plan(command)
        speak(response)
        
    # --- PHASE 1.8: OS OPERATIONS & APP LAUNCHER ---
    elif any(phrase in command for phrase in ["minimize all", "show desktop", "clear my screen"]):
        response = minimize_all_windows()
        speak(response)

    elif any(phrase in command for phrase in ["open", "launch", "start"]):
        app_response = launch_app(command)
        if app_response:
            speak(app_response)
        else:
            response = perform_web_search(command)
            speak(response)
        
    elif any(phrase in command for phrase in ["close", "terminate", "kill"]):
        response = close_app(command)
        speak(response)
        
    elif "search" in command:
        response = perform_web_search(command)
        speak(response)
        
    # --- PHASE 2: CONVERSATIONAL FALLBACK (THE AI BRAIN) ---
    else:
        if HAS_LLM:
            ai_response = process_with_llm(command, chat_history)
            chat_history += f"User: {command}\nSPIRIT: {ai_response}\n"
            
            if "```" in ai_response or len(ai_response) > 200:
                short_speech = "I have processed that request for you. The full documentation and code breakdown are rendered on your terminal screen."
                speak(short_speech, display_text=ai_response)
            else:
                speak(ai_response)
        else:
            speak("Active LLM API key required to complete this request.")

if __name__ == "__main__":
    status_msg = "AI Core Activated" if HAS_LLM else "Local Fallback"
    display_system_boot(status_msg)
    speak(f"System core initialized. Status: {status_msg}.")
    
    while True:
        wake_phrase = listen_for_wake_word()
        
        if "spirit" in wake_phrase:
            parts = wake_phrase.split("spirit", 1)
            command = parts[1].strip() if len(parts) > 1 else ""
            
            if command:
                display_user_input(wake_phrase)
                execute_skill(command)
            else:
                speak("At your service.")
                command = listen_command()
                if command:
                    execute_skill(command)
                    
            time.sleep(0.5)