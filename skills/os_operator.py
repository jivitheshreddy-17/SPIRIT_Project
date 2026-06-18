from AppOpener import open as app_open, close as app_close
import os
import subprocess

# --- SYSTEM OVERRIDES ---
# Native Windows commands that bypass AppOpener completely for 100% reliability
SYSTEM_LAUNCH_COMMANDS = {
    "microsoft store": "start ms-windows-store:",
    "store": "start ms-windows-store:",
    "settings": "start ms-settings:",
    "calculator": "calc",
    "notepad": "notepad",
    "file explorer": "explorer"
}

# Standard mappings for third-party software handled by AppOpener
APP_ALIASES = {
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "chrome": "google chrome",
    "edge": "microsoft edge",
    "word": "word",
    "excel": "excel",
    "powerpoint": "powerpoint"
}

def launch_app(command_text):
    """Parses the command, checks for system overrides, then falls back to AppOpener."""
    triggers = ["open", "launch", "start"]
    app_name = command_text
    
    for trigger in triggers:
        if f"{trigger} " in command_text:
            app_name = command_text.split(f"{trigger} ", 1)[1].strip()
            break
            
    if not app_name or app_name == command_text:
        return "Please specify which application you want me to open."

    clean_name = app_name.lower()

    # 1. Check for Native Windows System Overrides
    if clean_name in SYSTEM_LAUNCH_COMMANDS:
        try:
            # shell=True is required to execute native 'start' commands directly in cmd
            subprocess.Popen(SYSTEM_LAUNCH_COMMANDS[clean_name], shell=True)
            return f"Opening {app_name} via system protocol."
        except Exception:
            return f"Failed to execute system protocol for {app_name}."

    # 2. Check the Alias Dictionary for third-party apps
    target_app = APP_ALIASES.get(clean_name, app_name)

    try:
        app_open(target_app, match_closest=True, output=False)
        return f"Launching {target_app}."
    except Exception:
        return f"I could not locate or launch {target_app}."

def close_app(command_text):
    """Parses the command and closes the software."""
    triggers = ["close", "terminate", "kill"]
    app_name = command_text
    
    for trigger in triggers:
        if f"{trigger} " in command_text:
            app_name = command_text.split(f"{trigger} ", 1)[1].strip()
            break

    if not app_name or app_name == command_text:
        return "Please specify which application you want me to close."

    clean_name = app_name.lower()
    target_app = APP_ALIASES.get(clean_name, app_name)

    try:
        app_close(target_app, match_closest=True, output=False)
        return f"Terminating {target_app}."
    except Exception:
        return f"I could not close {target_app}."

def minimize_all_windows():
    """Uses a silent PowerShell command to instantly minimize all open windows."""
    try:
        os.system('powershell -command "(New-Object -ComObject shell.application).minimizeall()"')
        return "All windows minimized. Desktop is clear."
    except Exception:
        return "Failed to minimize open windows."