# backend/seed.py
from backend.database import init_db, insert_job, insert_resume

init_db()

# 1 sample JD
insert_job(1, "Data Analyst", "Python, SQL, Excel required")

# 10 sample resumes
sample_resumes = [
    {"id": i, "job_id": 1, "name": f"Candidate {i}", "college": f"College {i}", "location": "City", "resume_text": "Python SQL Excel"}
    for i in range(1, 11)
]

for r in sample_resumes:
    insert_resume(r["id"], r["job_id"], r["name"], r["college"], r["location"], r["resume_text"])
