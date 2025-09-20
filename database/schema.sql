-- database/schema.sql
PRAGMA foreign_keys = ON;

-- Jobs / Job Descriptions
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    location TEXT,
    source_file TEXT,      -- file name used to ingest
    must_have_skills TEXT, -- comma-separated or JSON string
    good_to_have_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    filepath TEXT,
    candidate_name TEXT,
    email TEXT,
    college TEXT,
    location TEXT,
    raw_text TEXT,         -- full parsed resume text
    parsed_json TEXT,      -- optional structured parse (json string)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evaluations (results of scoring a resume for a job)
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    resume_id INTEGER NOT NULL,
    relevance_score INTEGER,        -- 0..100
    verdict TEXT,                   -- 'High' / 'Medium' / 'Low'
    hard_match_score REAL,          -- 0..1
    semantic_score REAL,            -- 0..1
    missing_skills TEXT,            -- comma-separated or JSON
    feedback TEXT,                  -- LLM feedback / suggestions
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Simple audit log
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_evaluations_job_id ON evaluations(job_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_resume_id ON evaluations(resume_id);
