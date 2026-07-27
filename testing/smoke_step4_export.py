from storage.db_manager import DatabaseManager
from storage.exporter import ExcelExporter


def main():
    print("--- [STEP 4] Exporting Tasks to Excel ---")
    db = DatabaseManager()
    exporter = ExcelExporter(db)

    file_path = exporter.export_tasks_to_excel()
    print(f"Export successful! Created file: {file_path.resolve()}")

    print("\n>>> Open the generated Excel file to inspect both 'Metadata' and 'Tasks' sheets!")


if __name__ == "__main__":
    main()