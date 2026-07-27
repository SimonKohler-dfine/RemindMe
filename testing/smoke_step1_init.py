from storage.db_manager import DatabaseManager

def main():
    print("--- [STEP 1] Initializing Database Schema ---")
    db = DatabaseManager()
    print(f"Database created and schema initialized at: {db.db_path.resolve()}")
    print("\n>>> Open DBeaver or DuckDB Web UI to inspect empty tables and view_tasks.")

if __name__ == "__main__":
    main()