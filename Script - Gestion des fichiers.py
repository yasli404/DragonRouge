import os

def list_files(directory):
    print(f"Listing files in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            filesize = os.path.getsize(filepath)
            print(f"File: {filepath}, Size: {filesize} bytes")

if __name__ == "__main__":
    directory = "/path/to/directory"  # Remplacez par le répertoire à parcourir
    list_files(directory)