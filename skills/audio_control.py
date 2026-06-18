import re
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def adjust_volume(command_text):
    """Parses a spoken volume command and physically adjusts the Windows master volume."""
    try:
        # Modern pycaw (2024+) returns a clean wrapper, not the raw COM object
        device = AudioUtilities.GetSpeakers()
        
        # Bulletproof COM interface extraction
        try:
            # Attempt 1: New Pycaw syntax
            volume = device.EndpointVolume
            # If the wrapper lacks the scalar method, force a direct COM query
            if not hasattr(volume, 'SetMasterVolumeLevelScalar'):
                volume = device.EndpointVolume.QueryInterface(IAudioEndpointVolume)
        except AttributeError:
            # Attempt 2: Legacy Pycaw fallback syntax
            interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Check for mute/unmute commands first
        if "mute" in command_text and "unmute" not in command_text:
            volume.SetMute(1, None)
            return "System audio muted."
        elif "unmute" in command_text:
            volume.SetMute(0, None)
            return "System audio restored."

        # Extract the target percentage number from the spoken command
        numbers = re.findall(r'\d+', command_text)
        if not numbers:
            return "Please specify a volume percentage, like 50."
        
        # Clamp the value so we don't blow out your speakers
        target_vol = int(numbers[0])
        target_vol = max(0, min(100, target_vol))
        
        # Windows Audio API expects a decimal between 0.0 and 1.0
        scalar_volume = target_vol / 100.0
        volume.SetMasterVolumeLevelScalar(scalar_volume, None)
        
        # Ensure the system is unmuted when setting a specific volume
        volume.SetMute(0, None)
        
        return f"Volume adjusted to {target_vol} percent."
        
    except Exception as e:
        return f"Audio hardware interface failed. Error: {str(e)}"