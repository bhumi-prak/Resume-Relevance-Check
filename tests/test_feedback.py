from models.llm_feedback_model import generate_feedback

def test_feedback_generation():
    resume_text = "Experienced in Python, SQL, and Machine Learning."
    job_description = "Looking for a Data Scientist with Python, SQL, and AWS experience."
    missing_skills = ["AWS"]

    feedback = generate_feedback(resume_text, job_description, missing_skills)
    
    # Basic assertions
    assert isinstance(feedback, str), "Feedback should be a string"
    assert len(feedback) > 0, "Feedback should not be empty"
    assert "AWS" in feedback or "improve" in feedback.lower(), "Feedback should mention missing skills"
