import hashlib

def calculate_hash(file_path, algorithm='sha256'):
    if algorithm not in hashlib.algorithms_available:
        print(f"Error: Hashing algorithm {algorithm} not available.")