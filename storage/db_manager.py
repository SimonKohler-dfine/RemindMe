from pathlib import Path
import duckdb

class DatabaseManager:
    """Manages DuckDB connection lifecycle and initial schema creation."""

    def __init__(self, db_path: str = "remindme.duckdb") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Returns an active database connection."""
        return duckdb.connect(str(self.db_path))

    def _init_db(self) -> None:
        """Ensures required base tables exist upon initialization."""
        with self.get_connection() as con:
            # Staging table for raw imported Excel rows
            con.execute("""
                CREATE TABLE IF NOT EXISTS raw_imports (
                    import_id VARCHAR,
                    source_file VARCHAR,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payload JSON
                )
            """)

            # Processed tasks table ready for analytics and reminders
            con.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id VARCHAR PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    category VARCHAR,
                    duration_minutes INTEGER,
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)


if __name__ == "__main__":
    # Smoke test initialization
    db = DatabaseManager()
    print(f"Database initialized successfully at: {db.db_path.resolve()}")