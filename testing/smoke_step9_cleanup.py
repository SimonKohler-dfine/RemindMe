import sys
from pathlib import Path


def main():
    print("--- [STEP 9] Cleaning Up Database Files ---")
    db_file = Path("remindme.duckdb")

    # DuckDB creates auxiliary files (like WAL logs) alongside the main DB file
    files_to_remove = [
        db_file,
        Path(f"{db_file}.wal"),
        Path(f"{db_file}.tmp"),
    ]

    removed_count = 0
    for path in files_to_remove:
        if path.exists():
            try:
                path.unlink()
                print(f"Deleted: {path.name}")
                removed_count += 1
            except PermissionError:
                print(
                    f"\n[ERROR] Could not delete '{path.name}' because it is locked by another process.",
                    file=sys.stderr,
                )
                print(
                    "Please disconnect DBeaver or close the DuckDB Web UI, then run this script again.",
                    file=sys.stderr,
                )
                return

    if removed_count == 0:
        print("No database files found to clean up.")
    else:
        print("Cleanup complete. Database successfully reset!")


if __name__ == "__main__":
    main()