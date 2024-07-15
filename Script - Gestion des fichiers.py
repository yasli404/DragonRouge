import os
import hashlib
import magic
import math
from typing import Optional

def calculate_file_checksum(filename: str, block_size: int = 65536) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except IOError:
        return "Unable to read file"
def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy / 8

def check_encryption(file_path: str, threshold: float = 0.9) -> bool:
    try:
        with open(file_path, 'rb') as f:
            data = f.read(1024)  # Read first 1KB of the file
        return bool(data) and calculate_entropy(data) > threshold
    except IOError:
        return False

def get_file_type(path: str) -> str:
    try:
        return magic.from_file(path)
    except magic.MagicException:
        return "Unable to determine file type"

def check_file_corruption(path: str) -> bool:
    try:
        with open(path, 'rb') as f:
            f.read()
        return False
    except:
        return True

def process_file(path: str) -> Optional[dict]:
    try:
        return {
            "path": path,
            "size": os.path.getsize(path),
            "checksum": calculate_file_checksum(path),
            "type": get_file_type(path),
            "potentially_encrypted": check_encryption(path),
            "corrupted": check_file_corruption(path)
        }
    except Exception as e:
        print(f"Error processing file {path}: {str(e)}")
        return None
def listfiles(directory: str) -> None:
    for root, , files in os.walk(directory):
        for file in files:
            fileinfo = processfile(os.path.join(root, file))
            if fileinfo:
                print(f"File: {fileinfo['path']}")
                print(f"Size: {file_info['size']} bytes")
                print(f"SHA256: {file_info['checksum']}")
                print(f"Type: {file_info['type']}")
                print(f"Potentially Encrypted: {'Yes' if file_info['potentially_encrypted'] else 'No'}")
                print(f"Corrupted: {'Yes' if file_info['corrupted'] else 'No'}")
                print("---")

if __name == "__main":
    list_files('/home/')
