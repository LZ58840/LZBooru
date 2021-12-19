from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATABASE_FILE = "booru.db"  # sqlite specific
DATABASE_LOCATION = f"{PROJECT_ROOT}/{DATABASE_FILE}"  # sqlite specific
DATABASE_PLATFORM = "sqlite"
DATABASE_URI = f"{DATABASE_PLATFORM}:///{DATABASE_LOCATION}"