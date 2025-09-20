from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"
client = OpenAI()

def generate_feedback(resume_text, job_description, missing_skills):
    prompt = f"""
    Evaluate the resume below for this job description:

    Job Description:
    {job_description}

    Resume Text:
    {resume_text}

    Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}

    Provide concise feedback for improving the resume to better match the job.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
