import time
import threading
import os
import re
from datetime import datetime
import winsound

def _run_timer(total_seconds, display_time):
    """The background process that watches the clock."""
    time.sleep(total_seconds)
    
    # Play a soft double-beep alert (Frequency: 1000Hz, Duration: 800ms)
    winsound.Beep(1000, 800)
    time.sleep(0.2)
    winsound.Beep(1000, 800)
    
    # Log the session
    if not os.path.exists("data"):
        os.makedirs("data")
        
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    log_path = os.path.join("data", "pomodoro_logs.txt")
    
    with open(log_path, "a") as file:
        file.write(f"[{timestamp}] Completed a {display_time} focus session.\n")
        
    # Print a visible message to the terminal
    print(f"\n[SPIRIT ALERT] Your {display_time} focus timer is up! Session logged.")

def start_pomodoro(command_text):
    """Extracts hours, minutes, and seconds from the command and starts the timer."""
    
    # Use regex to find numbers followed by time-words
    hours_match = re.search(r'(\d+)\s*(hr|hour|hours)', command_text)
    mins_match = re.search(r'(\d+)\s*(min|mins|minute|minutes)', command_text)
    secs_match = re.search(r'(\d+)\s*(sec|secs|second|seconds)', command_text)
    
    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(mins_match.group(1)) if mins_match else 0
    seconds = int(secs_match.group(1)) if secs_match else 0
    
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    
    # Fallback: If they just say a number without a unit (e.g., "set a timer for 10")
    if total_seconds == 0:
        fallback_match = re.search(r'\b(\d+)\b', command_text)
        if fallback_match:
            minutes = int(fallback_match.group(1))
            total_seconds = minutes * 60
        else:
            return "I didn't catch how long you wanted the timer for. Please specify hours, minutes, or seconds."

    # Enforce the 2-hour limit (7200 seconds)
    if total_seconds > 7200:
        return "I can only set timers for up to 2 hours. Please request a shorter time."
        
    # Build a clean response string (e.g., "1 hour and 30 minutes")
    time_parts = []
    if hours > 0: time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0: time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0: time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    
    display_time = " and ".join(time_parts)

    # Start the timer in a background thread
    timer_thread = threading.Thread(target=_run_timer, args=(total_seconds, display_time))
    timer_thread.daemon = True
    timer_thread.start()
    
    return f"Timer set for {display_time}. Focus time starts now!"