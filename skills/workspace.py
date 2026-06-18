import os
import shutil

# Define the file categories and their corresponding extensions
EXTENSION_MAP = {
    'Code': ['.py', '.js', '.jsx', '.html', '.css', '.json', '.sh', '.bat', '.sql', '.cpp', '.c', '.java'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.md'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.ico', '.webp'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Media': ['.mp4', '.mp3', '.mkv', '.mov', '.wav', '.flac'],
    'Executables': ['.exe', '.msi']
}

def organize_folder(target_path):
    """Scans the target directory and sorts files into categorized folders."""
    if not os.path.exists(target_path):
        return f"Directory path does not exist: {target_path}"
        
    try:
        moved_counts = {}
        files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
        
        for file in files:
            file_path = os.path.join(target_path, file)
            _, ext = os.path.splitext(file.lower())
            
            # Identify the correct destination folder based on extension
            dest_folder = 'Others'
            for category, extensions in EXTENSION_MAP.items():
                if ext in extensions:
                    dest_folder = category
                    break
            
            # Create the category folder if it doesn't exist yet
            dest_dir = os.path.join(target_path, dest_folder)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                
            # Move the file safely
            shutil.move(file_path, os.path.join(dest_dir, file))
            moved_counts[dest_folder] = moved_counts.get(dest_folder, 0) + 1
            
        if not moved_counts:
            return "No loose files found to organize in that directory."
            
        summary = "Workspace cleanup complete. Sorted: "
        summary += ", ".join([f"{count} files into {folder}" for folder, count in moved_counts.items()])
        return summary
        
    except Exception as e:
        return f"Workspace automation error: {str(e)}"