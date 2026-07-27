import json
import uuid
from datetime import datetime
from storage.db_manager import DatabaseManager


class TaskProcessor:
    """Processes unhandled import batches into tasks using strict normalized keys."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def process_pending_imports(self) -> int:
        """Finds unprocessed import_ids, processes them under a unique process_id,
        and logs metadata to import_processing.
        """
        total_processed = 0

        with self.db_manager.get_connection() as con:
            # Identify import_ids not yet present in import_processing
            unprocessed_batches = con.execute("""
                SELECT DISTINCT import_id 
                FROM raw_imports 
                WHERE import_id NOT IN (
                    SELECT import_id FROM import_processing WHERE status = 'COMPLETED'
                )
            """).fetchall()

            if not unprocessed_batches:
                print("No pending imports to process.")
                return 0

            for (import_id,) in unprocessed_batches:
                # Generate a execution process ID
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                process_id = f"PRC_{timestamp_str}_{str(uuid.uuid4())[:4]}"

                rows = con.execute(
                    "SELECT payload FROM raw_imports WHERE import_id = ?",
                    (import_id,)
                ).fetchall()

                con.begin()
                try:
                    batch_count = 0
                    for (payload_str,) in rows:
                        payload = json.loads(payload_str)

                        task_id = str(uuid.uuid4())[:8]
                        title = payload.get("Title", "Untitled Task")
                        category = payload.get("Category", "General")
                        duration = int(payload.get("Duration", 0))

                        # Insert into normalized tasks table with process_id as FK
                        con.execute("""
                            INSERT INTO tasks (task_id, process_id, title, category, duration_minutes)
                            VALUES (?, ?, ?, ?, ?)
                        """, (task_id, process_id, title, category, duration))

                        batch_count += 1

                    # Log execution details with process_id as PK
                    con.execute("""
                        INSERT INTO import_processing (process_id, import_id, row_count, status)
                        VALUES (?, ?, ?, ?)
                    """, (process_id, import_id, batch_count, "COMPLETED"))

                    con.commit()
                    total_processed += batch_count
                    print(f"Processed import '{import_id}' under process_id '{process_id}' ({batch_count} rows).")

                except Exception as e:
                    con.rollback()
                    con.execute("""
                        INSERT INTO import_processing (process_id, import_id, row_count, status)
                        VALUES (?, ?, ?, ?)
                    """, (process_id, import_id, 0, f"FAILED: {str(e)}"))
                    raise RuntimeError(f"Processing batch {import_id} failed: {e}") from e

        return total_processed


if __name__ == "__main__":
    db = DatabaseManager()
    processor = TaskProcessor(db)
    count = processor.process_pending_imports()
    print(f"Total tasks processed in run: {count}")