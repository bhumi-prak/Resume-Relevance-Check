import os
import shutil
from backend.logger import get_logger

logger = get_logger("cleanup")

# Delete temp embeddings (if stored as files)
EMBEDDING_DIR = "data/embeddings"
if os.path.exists(EMBEDDING_DIR):
    shutil.rmtree(EMBEDDING_DIR)
    logger.info("Deleted embeddings directory")

# Clear logs (optional)
LOG_DIR = "logs"
for f in os.listdir(LOG_DIR):
    file_path = os.path.join(LOG_DIR, f)
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info(f"Deleted log file {f}")

print("Cleanup completed.")
