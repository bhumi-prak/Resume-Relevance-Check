from openai import OpenAI
import os
from backend.logger import get_logger

logger = get_logger("feedback")


os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"  # or use .env

client = OpenAI()

def generate_feedback(resume_text, job_description, missing_skills):
    prompt = f"""
    The resume below is being evaluated for this job description:
    {job_description}

    Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}

    Give concise feedback on how the candidate can improve the resume to better match the JD.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
