import os
from dotenv import load_dotenv

# Load environment variables from .env file
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
load_dotenv(f".env.{ENVIRONMENT}", override=True)

# Get environment variables or use default values
DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "admin123")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# Construct the connection string
CONNECTION_STRING = f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD} host={DATABASE_HOST} port={DATABASE_PORT}"

MODE = os.getenv("MODE", "Development")
DEBUG = os.getenv("DEBUG", True)