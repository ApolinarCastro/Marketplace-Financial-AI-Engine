import sqlite3
import glob
import sys

def check_db(filename):
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        return result[0] if result else "unknown"
    except sqlite3.DatabaseError as e:
        return f"CORRUPTED or NOT A DB: {e}"
    except Exception as e:
        return f"ERROR: {e}"

def main():
    files = glob.glob('*.db') + glob.glob('*.sqlite*')
    for f in files:
        print(f"{f}: {check_db(f)}")

if __name__ == '__main__':
    main()
