import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_PATH = os.getenv("DB_PATH", "./database/resume_checker.db")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./database/vector_index")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
