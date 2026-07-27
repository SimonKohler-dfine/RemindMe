import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from storage.db_manager import DatabaseManager


class ExcelImporter:
    """Handles parsing Excel files and staging raw records into DuckDB."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def import_excel(self, file_path: str | Path) -> str:
        """Reads an Excel sheet and stages its rows into raw_imports.

        Returns the unique import_id generated for this run.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")

        df = pd.read_excel(path)
        records = df.to_dict(orient="records")

        # Generate a unique batch ID per import run
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        import_id = f"IMP_{timestamp_str}_{path.stem}"
        source_name = path.name

        with self.db_manager.get_connection() as con:
            con.begin()
            try:
                for row in records:
                    payload_json = json.dumps(row, default=str)
                    con.execute(
                        """
                        INSERT INTO raw_imports (import_id, source_file, payload)
                        VALUES (?, ?, ?)
                        """,
                        (import_id, source_name, payload_json),
                    )
                con.commit()
            except Exception as e:
                con.rollback()
                raise RuntimeError(f"Failed to stage Excel data: {e}") from e

        return import_id


if __name__ == "__main__":
    test_file = Path("test_tasks.xlsx")
    sample_data = pd.DataFrame([
        {"Title": "Vault Architecture Test", "Category": "Dev", "Duration": 60},
        {"Title": "Configure Logging", "Category": "Dev", "Duration": 20},
    ])
    sample_data.to_excel(test_file, index=False)

    db = DatabaseManager()
    importer = ExcelImporter(db)
    batch_id = importer.import_excel(test_file)

    print(f"Successfully staged batch '{batch_id}' into raw_imports.")

    if test_file.exists():
        test_file.unlink()