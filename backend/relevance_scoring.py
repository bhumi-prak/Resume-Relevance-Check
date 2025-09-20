from backend.database import insert_evaluation, get_resumes_for_job, get_jobs
from backend.embeddings import get_embedding, cosine_similarity
from backend.feedback_generator import generate_feedback
from backend.parsing import extract_text
from backend.logger import get_logger

logger = get_logger("scoring")


# Example hard skills list (can be extracted from JD dynamically)
HARDCODED_SKILLS = ["Python", "SQL", "AWS", "React", "Machine Learning"]

def evaluate_resume_for_job(resume_id, job_id, resume_file=None, jd_file=None):
    """
    Evaluates a resume against a job description.

    Parameters:
        resume_id: int
        job_id: int
        resume_file: str (path to resume file)
        jd_file: str (path to JD file)
    Returns:
        dict with score, verdict, missing_skills, feedback, resume_text, name, college, location
    """

    # 1️⃣ Load resume text
    if resume_file:
        resume_text = extract_text(resume_file)
    else:
        resumes = get_resumes_for_job(job_id, verdicts=["High","Medium","Low"])
        resume_data = next((r for r in resumes if r['id'] == resume_id), None)
        if resume_data:
            resume_text = resume_data['resume_text']
        else:
            resume_text = ""

    # 2️⃣ Load job description
    if jd_file:
        job_description = extract_text(jd_file)
    else:
        jobs = get_jobs()
        job = next((j for j in jobs if j['id'] == job_id), None)
        job_description = job.get('description', "") if job else ""

    # 3️⃣ Hard match - check skills
    missing_skills = [skill for skill in HARDCODED_SKILLS if skill.lower() not in resume_text.lower()]
    hard_score = int((len(HARDCODED_SKILLS) - len(missing_skills)) / len(HARDCODED_SKILLS) * 50)  # 50% weight

    # 4️⃣ Semantic match - embeddings cosine similarity
    try:
        emb_resume = get_embedding(resume_text)
        emb_jd = get_embedding(job_description)
        sem_score = cosine_similarity(emb_resume, emb_jd) * 50  # 50% weight
    except Exception as e:
        print(f"[Semantic Match Error]: {e}")
        sem_score = 0

    # 5️⃣ Total score
    total_score = int(hard_score + sem_score)

    # 6️⃣ Verdict
    if total_score >= 70:
        verdict = "High"
    elif total_score >= 40:
        verdict = "Medium"
    else:
        verdict = "Low"

    # 7️⃣ Generate LLM feedback
    feedback = generate_feedback(resume_text, job_description, missing_skills)

    # 8️⃣ Save evaluation in DB
    insert_evaluation(
        resume_id,
        job_id,
        total_score,
        verdict,
        missing_skills,
        feedback
    )

    # 9️⃣ Return data for dashboard
    return {
        "score": total_score,
        "verdict": verdict,
        "missing_skills": missing_skills,
        "feedback": feedback,
        "resume_text": resume_text,
        "name": resume_data['name'] if resume_data else "Candidate Name",
        "college": resume_data['college'] if resume_data else "Candidate College",
        "location": resume_data['location'] if resume_data else "Candidate Location"
    }
