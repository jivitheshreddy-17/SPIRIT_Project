import os

def get_installed_apps():
    """Silently scans the Windows Start Menu and Desktop to build an index of all installed apps."""
    
    # We include a few hidden Windows core tools that don't always have normal shortcuts
    apps = {
        "calculator": "calc",
        "command prompt": "cmd",
        "terminal": "wt",
        "settings": "start ms-settings:",
        "file explorer": "explorer"
    }
    
    # These are the standard hidden folders where Windows stores application shortcuts
    paths = [
        os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), r'Microsoft\Windows\Start Menu\Programs'),
        os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    ]
    
    for path in paths:
        if not os.path.exists(path):
            continue
            
        # Walk through every folder and sub-folder looking for shortcuts (.lnk files)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    # Clean up the filename to get just the app's name
                    app_name = file.replace(".lnk", "").lower()
                    apps[app_name] = os.path.join(root, file)
                    
    return apps

# Build the index in the background the moment this module is loaded
APP_INDEX = get_installed_apps()

def launch_app(command_text):
    """Dynamically matches the spoken word to the scanned application index."""
    
    words = command_text.split()
    
    # Isolate the name of the app the user wants to open
    if "open" in words:
        target_app = " ".join(words[words.index("open") + 1:]).strip()
    elif "launch" in words:
        target_app = " ".join(words[words.index("launch") + 1:]).strip()
    else:
        return None

    if not target_app:
        return None

    # Search our dynamic index for a fuzzy match
    for app_name, app_path in APP_INDEX.items():
        # E.g., if you say "chrome", it will match the shortcut named "google chrome"
        if target_app in app_name:
            try:
                # If it's a core Windows tool (like 'calc')
                if not app_path.endswith('.lnk'):
                    os.system(app_path)
                # If it's a standard scanned application path
                else:
                    os.startfile(app_path)
                return f"Opening {app_name}"
            except Exception:
                return "I found the app, but encountered an error trying to launch it."

    # If the app isn't found on the computer, return None so the Brain passes it to Web Search
    return None