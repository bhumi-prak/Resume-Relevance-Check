Resume Relevance Check

Automated Resume Relevance Check System — a Streamlit-based web app that helps recruiters and placement teams evaluate candidate resumes against job descriptions.
It combines rule-based parsing, semantic similarity (embeddings), and AI feedback generation to provide structured evaluations.


Features

Upload job descriptions (TXT/PDF/DOCX) and candidate resumes (PDF/DOCX).

Extract and parse text content from resumes using pdfplumber / python-docx.

Compare resumes with job descriptions using:

Keyword & fuzzy matching

Semantic similarity (embeddings + cosine similarity)

Generate evaluation scores (0–100) with verdicts (High, Medium, Low).

Store results in SQLite database for reproducibility.

View analytics dashboard with charts, filters, and shortlisting options.

Modular backend (backend/) and frontend (frontend/) design for extensibility.

🛠️ Tech Stack

Frontend: Streamlit

Backend: Python (modular services for parsing, scoring, embeddings, feedback)

Database: SQLite3

Parsing: pdfplumber, python-docx

Embeddings & AI: OpenAI API (can be swapped with HuggingFace / Gemini)

Analytics: Altair, Pandas



⚙️ Installation
1. Clone the repo
git clone https://github.com/your-username/Resume-Relevance-Check.git
cd Resume-Relevance-Check/ResumeMatcher

2. Install dependencies
pip install -r requirements.txt

3. Run Streamlit app
streamlit run app.py


App will start at http://localhost:8501

▶️ Usage

Open the app in your browser.

Create a Job

Select a template or paste/upload a Job Description.

Save it to the database.

Upload Resumes (PDF/DOCX).

Evaluate

Select a job and run evaluation.

View results in table + charts.

Export shortlisted candidates to CSV.

🔮 Future Enhancements

Use embeddings (OpenAI, HuggingFace, Gemini) for semantic similarity.

Personalized suggestions using LLMs.

Role-based access: Students vs Admin Dashboard.

Integration with vector databases (FAISS/Chroma/Pinecone).