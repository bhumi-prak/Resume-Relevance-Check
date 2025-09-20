import json
from backend.embeddings import get_embedding
from backend.database import get_jobs, get_resumes_for_job, insert_embedding
from backend.logger import get_logger

logger = get_logger("generate_embeddings")

def main():
    # Load jobs and resumes from database
    jobs = get_jobs()
    
    for job in jobs:
        try:
            emb = get_embedding(job['description'])
            insert_embedding(item_id=job['id'], item_type='job', embedding=emb)
            logger.info(f"Generated embedding for job {job['title']}")
        except Exception as e:
            logger.error(f"Failed for job {job['id']}: {e}")

    resumes = get_resumes_for_job(job_id=None)  # Fetch all resumes
    for resume in resumes:
        try:
            emb = get_embedding(resume['resume_text'])
            insert_embedding(item_id=resume['id'], item_type='resume', embedding=emb)
            logger.info(f"Generated embedding for resume {resume['name']}")
        except Exception as e:
            logger.error(f"Failed for resume {resume['id']}: {e}")

if __name__ == "__main__":
    main()
