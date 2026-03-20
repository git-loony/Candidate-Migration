import os
from dotenv import load_dotenv

load_dotenv()

MANATAL_API_KEY = os.getenv("MANATAL_API_KEY")
ASHBY_API_KEY = os.getenv("ASHBY_API_KEY")

PER_PAGE = int(os.getenv("PER_PAGE", 10))
API_SLEEP = float(os.getenv("API_SLEEP", 1))

DB_FILE = "migration.db"
LOG_EXPORT_FILE = "logs/migration_log.csv"
RESUME_FOLDER = "resumes"

# -test-
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
print("Mock_mode: ", MOCK_MODE)