import re

SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c", "cplusplus", "csharp",
    "r", "scala", "kotlin", "swift", "go", "rust", "php", "ruby", "matlab",
    "perl", "bash", "shell", "sql",
    "html", "css", "react", "angular", "vue", "nextjs", "nodejs", "express",
    "django", "flask", "fastapi", "spring", "bootstrap", "tailwind",
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "opencv", "hugging face",
    "transformers", "bert", "gpt", "llm", "data analysis", "data science",
    "feature engineering", "model training", "model deployment",
    "neural network", "regression", "classification", "clustering",
    "random forest", "xgboost", "gradient boosting",
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "cassandra", "elasticsearch", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "github actions", "ci/cd", "linux", "git", "github", "gitlab",
    "rest api", "graphql", "microservices",
    "excel", "power bi", "tableau", "jira", "agile", "scrum",
    "unit testing", "pytest", "selenium", "hadoop", "spark", "airflow",
    "streamlit", "jupyter", "postman",
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "project management",
]

def extract_skills(text, skills_list=None):
    if skills_list is None:
        skills_list = SKILLS_DB
    text_lower = text.lower()
    text_lower = text_lower.replace('c++', 'cplusplus').replace('c#', 'csharp').replace('.net', 'dotnet')
    found = []
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def get_skill_gap(resume_text, jd_text):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)
    return matched, missing, extra