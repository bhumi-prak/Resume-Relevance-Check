from backend.relevance_scoring import evaluate_resume_for_job

def test_relevance_evaluation():
    # Example paths to sample data
    resume_file = "data/resumes/resume1.pdf"
    jd_file = "data/jobs/job1.pdf"

    result = evaluate_resume_for_job(
        resume_id=1,
        job_id=1,
        resume_file=resume_file,
        jd_file=jd_file
    )

    # Assertions to check structure
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "score" in result, "Result must contain 'score'"
    assert "verdict" in result, "Result must contain 'verdict'"
    assert "missing_skills" in result, "Result must contain 'missing_skills'"
    assert "feedback" in result, "Result must contain 'feedback'"

    # Optional: check score range
    assert 0 <= result['score'] <= 100, "Score must be between 0 and 100"
