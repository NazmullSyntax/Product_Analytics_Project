import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Find the root directory (one level up from src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from the root directory
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Get the full connection string
DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    """Returns a SQLAlchemy engine connected to the Neon Cloud PostgreSQL."""
    if not DATABASE_URL:
        raise ValueError(f"❌ DATABASE_URL is not set. Checked .env at: {env_path}")
    return create_engine(DATABASE_URL)