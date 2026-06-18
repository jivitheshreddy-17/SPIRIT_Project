import psutil
import screen_brightness_control as sbc
import subprocess

def get_system_status():
    """Reads hardware sensors for CPU, Memory, and Battery."""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram_usage = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        report = f"System diagnostics: CPU load is at {cpu_usage} percent. Memory usage is at {ram_usage} percent."
        
        if battery:
            plug_status = "plugged into AC power" if battery.power_plugged else "running on battery"
            report += f" The battery is at {battery.percent} percent and is currently {plug_status}."
        else:
            report += " No battery sensor detected."
            
        return report
    except Exception as e:
        return f"Hardware sensor error: {str(e)}"

def adjust_brightness(command_text):
    """Sets the screen brightness based on spoken percentage."""
    try:
        words = command_text.split()
        target_level = None
        for word in words:
            clean_word = word.replace('%', '')
            if clean_word.isdigit():
                target_level = int(clean_word)
                break
                
        if target_level is not None:
            target_level = max(0, min(100, target_level))
            sbc.set_brightness(target_level)
            return f"Display brightness adjusted to {target_level} percent."
        else:
            return "I did not catch a specific percentage for the brightness adjustment."
    except Exception as e:
        return f"Display control error: {str(e)}"

def set_power_plan(command_text):
    """Uses Windows powercfg to switch power modes."""
    try:
        if "saver" in command_text or "saving" in command_text:
            subprocess.run(["powercfg", "/setactive", "a1841308-3541-4fab-bc81-f71556f20b4a"], capture_output=True)
            return "Power plan set to Battery Saver."
        elif "performance" in command_text or "high" in command_text:
            subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"], capture_output=True)
            return "Power plan set to High Performance."
        elif "balanced" in command_text or "normal" in command_text:
            subprocess.run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], capture_output=True)
            return "Power plan set to Balanced."
        else:
            return "Please specify if you want power saver, balanced, or high performance mode."
    except Exception as e:
        return f"Power plan error: {str(e)}"