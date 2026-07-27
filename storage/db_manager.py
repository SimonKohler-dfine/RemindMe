from pathlib import Path
import duckdb


class DatabaseManager:
    """Manages DuckDB connection lifecycle, normalized schema, and presentation views."""

    def __init__(self, db_path: str = "remindme.duckdb") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Returns an active database connection."""
        return duckdb.connect(str(self.db_path))

    def _init_db(self) -> None:
        """Ensures normalized tables and views exist upon initialization."""
        with self.get_connection() as con:
            # 1. Immutable Raw Vault
            con.execute("""
                CREATE TABLE IF NOT EXISTS raw_imports (
                    import_id VARCHAR,
                    source_file VARCHAR,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payload JSON
                )
            """)

            # 2. Execution tracking (process_id = Primary Key)
            con.execute("""
                CREATE TABLE IF NOT EXISTS import_processing (
                    process_id VARCHAR PRIMARY KEY,
                    import_id VARCHAR,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    row_count INTEGER,
                    status VARCHAR
                )
            """)

            # 3. Normalized tasks table
            con.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id VARCHAR PRIMARY KEY,
                    process_id VARCHAR,
                    title VARCHAR NOT NULL,
                    category VARCHAR,
                    duration_minutes INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 4. Presentation view combining tasks with import metadata
            con.execute("""
                CREATE VIEW IF NOT EXISTS view_tasks AS
                SELECT 
                    t.task_id,
                    t.process_id,
                    ip.import_id,
                    t.title,
                    t.category,
                    t.duration_minutes,
                    t.created_at
                FROM tasks t
                JOIN import_processing ip ON t.process_id = ip.process_id
            """)