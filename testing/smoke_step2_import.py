from pathlib import Path
import pandas as pd
from storage.db_manager import DatabaseManager
from storage.importer import ExcelImporter


def main():
    print("--- [STEP 2] Importing Sample Excel File ---")

    imports_dir = Path("imports")
    imports_dir.mkdir(parents=True, exist_ok=True)

    sample_file = imports_dir / "sample_data.xlsx"
    df = pd.DataFrame([
        {"Title": "Refactor Codebase", "Category": "Architecture", "Duration": 45},
        {"Title": "Verify DBeaver Connection", "Category": "Testing", "Duration": 15},
        {"Title": "Draft Documentation", "Category": "Docs", "Duration": 30},
    ])
    df.to_excel(sample_file, index=False)

    db = DatabaseManager()
    importer = ExcelImporter(db)
    import_id = importer.import_excel(sample_file)
    print(f"Excel file staged successfully under batch ID: {import_id}")

    # Clean up test file inside imports/
    if sample_file.exists():
        sample_file.unlink()

    print("\n>>> Open DBeaver/Web UI: Query 'raw_imports' to see the unparsed JSON landing zone!")


if __name__ == "__main__":
    main()