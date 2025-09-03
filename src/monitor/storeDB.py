import sqlite3
import logging

def check_stored_hashes():
    """Connects to the SQLite database and prints all stored file hashes."""
    conn = None
    try:
        conn = sqlite3.connect('hashing_data.db')
        cursor = conn.cursor()
        
        # Execute the query to get all records from the file_hashes table
        cursor.execute("SELECT id, path, hash_value, algorithm, created_at FROM file_hashes")
        
        records = cursor.fetchall()
        
        if not records:
            logging.info("No records found in the database.")
            return

        print("\n--- Stored File Hashes ---")
        for row in records:
            print(f"ID: {row[0]}, Path: {row[1]}, Hash: {row[2]}, Algorithm: {row[3]}, Created At: {row[4]}")
        print("--------------------------")
        
    except sqlite3.Error as e:
        logging.error(f"Failed to read from SQLite database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_stored_hashes()