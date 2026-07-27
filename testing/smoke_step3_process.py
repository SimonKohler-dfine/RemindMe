from storage.db_manager import DatabaseManager
from storage.processor import TaskProcessor


def main():
    print("--- [STEP 3] Processing Staged Raw Imports ---")
    db = DatabaseManager()
    processor = TaskProcessor(db)

    count = processor.process_pending_imports()
    print(f"Processed {count} rows into domain models.")

    print(
        "\n>>> Open DBeaver/Web UI: Query 'import_processing', 'tasks', and 'view_tasks' to inspect full relational data!")


if __name__ == "__main__":
    main()