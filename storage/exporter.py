from datetime import datetime
from pathlib import Path
import pandas as pd
from storage.db_manager import DatabaseManager


class ExcelExporter:
    """Handles querying presentation views and exporting to multi-sheet Excel workbooks."""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    def export_tasks_to_excel(self, output_dir: str | Path = "exports") -> Path:
        """Queries view_tasks and writes a 2-sheet Excel file (Metadata & Tasks) to exports/.

        Returns the path to the generated Excel file.
        """
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1. Fetch task records directly from the presentation view
        with self.db_manager.get_connection() as con:
            tasks_df = con.execute("SELECT * FROM view_tasks").df()

        # 2. Construct Metadata sheet structure
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata_df = pd.DataFrame([
            {"Property": "Export Timestamp", "Value": now_str},
            {"Property": "Creator", "Value": "Dummy"},
            {"Property": "Sheets", "Value": "Metadata, Tasks"},
            {"Property": "Total Records", "Value": len(tasks_df)},
        ])

        # 3. Create timestamped output filename
        file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file_path = out_dir / f"tasks_export_{file_timestamp}.xlsx"

        # 4. Write multi-sheet Excel file via pandas ExcelWriter
        with pd.ExcelWriter(export_file_path, engine="openpyxl") as writer:
            metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
            tasks_df.to_excel(writer, sheet_name="Tasks", index=False)

        return export_file_path