print("1. Testing basic modules...")
import sys
import time
import os

print("2. Testing Speech Recognition (Microphone)...")
import speech_recognition as sr

print("3. Testing Voice Engine...")
import pyttsx3

print("4. Testing LLM Brain...")
from skills.llm_brain import process_with_llm, HAS_LLM

print("5. Testing Workspace...")
from skills.workspace import organize_folder

print("6. Testing OS Operator (AppOpener)...")
from skills.os_operator import launch_app, close_app, minimize_all_windows

print("7. Testing Vitals (psutil / brightness)...")
from skills.vitals import get_system_status, adjust_brightness, set_power_plan

print("8. Testing Vision...")
from skills.vision import analyze_screen

print("9. Testing Terminal UI...")
from skills.terminal_ui import display_system_boot

print("\n[SUCCESS] ALL IMPORTS PASSED! The crash is not an import issue.")