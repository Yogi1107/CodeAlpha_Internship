import os
import shutil

# Set the path to your Downloads folder (adjust for your system)
downloads_folder = os.path.expanduser("~/Downloads")

# Define the destination folders based on file extensions
file_mappings = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh"],
}

def organize_files():
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()

            for folder, extensions in file_mappings.items():
                if file_ext in extensions:
                    target_folder = os.path.join(downloads_folder, folder)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f"Moved {filename} to {folder}/")
                    break

if __name__ == "__main__":
    organize_files()
