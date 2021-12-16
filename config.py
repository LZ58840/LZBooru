from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATABASE_FILE = "booru.db"
DATABASE_LOCATION = f"sqlite:///{PROJECT_ROOT}/{DATABASE_FILE}"