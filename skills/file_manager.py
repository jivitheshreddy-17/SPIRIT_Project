import os
import shutil
from datetime import datetime

def take_note(command_text):
    """Extracts the note content and saves it directly to the Windows Desktop."""
    
    triggers = ["note down", "take a note", "save note", "record this", "write this down"]
    note_content = command_text
    
    # 1. Strip the trigger phrase
    for trigger in triggers:
        if trigger in command_text:
            parts = command_text.split(trigger, 1)
            if len(parts) > 1:
                note_content = parts[1].strip()
                break
    
    # 2. Clean up grammar
    if note_content.startswith("that "):
        note_content = note_content[5:].strip()
    elif note_content.startswith("to "):
        note_content = note_content[3:].strip()
        
    if not note_content:
        return "I am ready. What would you like me to write down?"

    # 3. Target the Windows Desktop dynamically
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "SPIRIT_Notes.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    # 4. Save the file
    try:
        with open(filename, "a") as file:
            file.write(f"[{timestamp}] {note_content.capitalize()}\n")
        # Updated verbal response to confirm location
        return "Note saved successfully to your Desktop."
    except Exception as e:
        return f"Error saving note: {str(e)}"

def get_target_directory(command_text):
    """Finds the requested Windows directory mentioned in the command."""
    base_dir = os.path.expanduser('~')
    locations = {
        "desktop": os.path.join(base_dir, "Desktop"),
        "downloads": os.path.join(base_dir, "Downloads"),
        "documents": os.path.join(base_dir, "Documents")
    }
    for loc, path in locations.items():
        if loc in command_text:
            return path, loc
    return None, None

def manage_files(command_text):
    """Dynamically handles creating, deleting, and cleaning files/folders."""
    target_path, loc_name = get_target_directory(command_text)
    
    if not target_path:
        return "I couldn't understand which folder you meant. Please specify Desktop, Downloads, or Documents."

    words = command_text.split()

    # ACTION 1: CREATE A FOLDER
    if "create" in command_text and "folder" in command_text:
        # Tries to find the word spoken right after "named", "naming", or "folder"
        name = ""
        if "named" in words: name = words[words.index("named") + 1]
        elif "naming" in words: name = words[words.index("naming") + 1]
        elif "folder" in words:
            idx = words.index("folder")
            if idx + 1 < len(words) and words[idx+1] not in ["in", "on", "at"]:
                name = words[idx+1]

        if not name:
            return "I didn't catch the name of the folder you want to create."
            
        new_dir = os.path.join(target_path, name)
        try:
            os.makedirs(new_dir, exist_ok=True)
            return f"Successfully created folder {name} on your {loc_name}."
        except Exception as e:
            return f"Failed to create folder. Error: {str(e)}"

    # ACTION 2: DELETE A FILE OR FOLDER
    elif "delete" in command_text or "remove" in command_text:
        try:
            # Find the word spoken right after "file" or "folder"
            target_type = "folder" if "folder" in command_text else "file"
            if target_type in words:
                start_idx = words.index(target_type) + 1
                # Find the end of the name (usually before the word "in" or "on")
                end_idx = words.index("in") if "in" in words else len(words)
                if "on" in words and words.index("on") < end_idx: end_idx = words.index("on")
                
                target_name = " ".join(words[start_idx:end_idx]).strip()
                
                # Fix common speech recognition quirks (e.g. "test dot cpp" -> "test.cpp")
                target_name = target_name.replace(" dot ", ".")
            else:
                return f"Please specify if you want to delete a file or a folder."
                
            if not target_name:
                return "I didn't catch the name of the item to delete."

            full_target_path = os.path.join(target_path, target_name)
            
            if not os.path.exists(full_target_path):
                return f"I could not find {target_name} on your {loc_name}."

            if os.path.isdir(full_target_path):
                shutil.rmtree(full_target_path) # Deletes folder and everything inside
                return f"Successfully deleted the folder {target_name}."
            else:
                os.remove(full_target_path) # Deletes file
                return f"Successfully deleted the file {target_name}."
                
        except Exception as e:
             return "I encountered an error trying to delete that item. It might be currently open."

    return "I found the location, but I didn't understand the action you wanted to take."