import os
import hashlib
import logging
from typing import List
import sys
import sqlite3

# Configure basic logging to provide informative output.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _hash_file(filepath: str, algorithm: str) -> str:
    """
    Hashes a single file in chunks to be memory-efficient.

    Args:
        filepath (str): The path to the file.
        algorithm (str): The hashing algorithm to use.

    Returns:
        str: The hexadecimal hash of the file, or an error message.
    """
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):  
                hasher.update(chunk)
        return hasher.hexdigest()
    except OSError as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return f"Error: Failed to hash file."

def _hash_directory(folder_path: str, algorithm: str) -> str:
    """
    Hashes a directory by combining the hashes of its files.
    
    This method ensures a consistent hash by sorting file names
    before hashing their combined content.

    Args:
        folder_path (str): The path to the directory.
        algorithm (str): The hashing algorithm to use.

    Returns:
        str: The hexadecimal hash of the directory, or an error message.
    """
    hasher = hashlib.new(algorithm)
    file_hashes: List[str] = []
    
    # Use os.walk to traverse the directory, sorting files for consistent hashes
    for root, _, files in os.walk(folder_path, onerror=lambda e: logging.error(f"Error accessing: {e}")):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            file_hash = _hash_file(filepath, algorithm)
            
            if not file_hash.startswith("Error"):
                file_hashes.append(file_hash)
            else:
                logging.warning(f"Skipping {filepath} due to a hashing error.")
                
    # Create a consistent hash for the directory by hashing the sorted file hashes
    combined_string = "".join(sorted(file_hashes))
    hasher.update(combined_string.encode('utf-8'))
    return hasher.hexdigest()

def hash_data(path: str, algorithm: str = 'sha256') -> str:
    """
    Hashes a file or folder using the specified algorithm.

    Args:
        path (str): The path to the file or folder.
        algorithm (str): The hashing algorithm to use (e.g., 'sha256', 'sha512').

    Returns:
        str: The hexadecimal hash of the data, or an error message.
    """
    if not os.path.exists(path):
        return f"Error: The path '{path}' does not exist."
    
    if algorithm not in hashlib.algorithms_available:
        return f"Error: Unsupported hashing algorithm '{algorithm}'."

    if os.path.isfile(path):
        return _hash_file(path, algorithm)
    elif os.path.isdir(path):
        return _hash_directory(path, algorithm)
    else:
        return f"Error: The path '{path}' is not a file or directory."

def store_hash_in_sqlite(path: str, hash_value: str, algorithm: str):
    """
    Stores the hash value in an SQLite database file.
    
    This function will automatically create the 'hashing_data.db' file
    and the 'file_hashes' table if they don't already exist.

    Args:
        path (str): The file or folder path.
        hash_value (str): The calculated hash value.
        algorithm (str): The hashing algorithm used.
    """
    conn = None
    try:
        # Connect to the SQLite database file. It will be created if it doesn't exist.
        conn = sqlite3.connect('hashing_data.db')
        cursor = conn.cursor()

        # Create the table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(255) NOT NULL,
                hash_value VARCHAR(255) NOT NULL,
                algorithm VARCHAR(50) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # SQL INSERT statement using a parameterized query for security
        sql = """
        INSERT INTO file_hashes (path, hash_value, algorithm)
        VALUES (?, ?, ?);
        """
        cursor.execute(sql, (path, hash_value, algorithm))

        conn.commit()
        logging.info(f"Hash value successfully stored in SQLite for path: {path}")

    except sqlite3.Error as e:
        logging.error(f"Failed to connect to or store data in SQLite: {e}")
        if conn:
            conn.rollback()  
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Prompt the user for input instead of using command-line arguments
    path = input("Enter the path to the file or folder: ").strip('\'" ')
    algorithm = input("Enter the hashing algorithm (e.g., 'sha256', 'sha512', default is sha256): ")
    if not algorithm:
        algorithm = "sha256"
    
    hash_value = hash_data(path, algorithm)
    print(f"Hash for {path}: {hash_value}")
    
    if not hash_value.startswith("Error"):
        store_hash_in_sqlite(path, hash_value, algorithm)
    else:
        print("Hash could not be computed. Not storing in the database.")
