# 🤖 AI-Based Resume Screening System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%2B%20NLTK-green?style=for-the-badge)
![ML](https://img.shields.io/badge/ML-Sentence%20Transformers-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**An intelligent AI-powered resume screening system that automatically ranks job candidates using NLP and Machine Learning.**

</div>

---

## 👨‍💻 Author

**Ketan Rokade**
- 🎓 Computer Science & AI/ML Engineer
- 💼 Built as a capstone project demonstrating real-world NLP, ML, and full-stack Python skills
- 📧 Contact via GitHub

---

## 📌 Project Overview

Traditional resume screening is slow, biased, and inconsistent. HR teams spend hours reading hundreds of resumes manually.

This system solves that problem using:
- **Sentence Transformers (BERT-based)** to understand the *meaning* of resume text
- **Cosine Similarity** to match resumes against a job description
- **NLP Skill Extraction** to find matched and missing skills
- **ATS Scoring** to check how resume-friendly each candidate's document is
- **Streamlit Web UI** to visualize everything in a clean dashboard

---

## ✨ Features

### 📄 Resume Processing
- Upload multiple PDF or DOCX resumes at once
- Auto-extract candidate Name, Email, Phone, LinkedIn
- Education level detection (B.Tech, M.Tech, MBA, PhD etc.)
- Experience years extraction
- Resume formatting and ATS-friendliness check

### 🧠 AI-Powered Matching
- Sentence Transformer embeddings (`all-MiniLM-L6-v2`)
- Cosine similarity scoring (0–100%)
- Semantic understanding — "ML" matches "machine learning"
- Keyword density analysis

### 🎯 Skill Analysis
- 100+ skills tracked across programming, ML, cloud, DevOps, databases
- Matched skills (green), Missing skills (red), Bonus skills (blue)
- Skill coverage heatmap across all candidates
- Most commonly missing skills chart

### 🏆 Ranking Engine
- Candidates sorted by match score
- Configurable minimum threshold filter
- Top N candidates display
- Gold / Silver / Bronze medals for top 3

### 💼 Job Role Presets
- Data Analyst
- ML Engineer
- Backend Developer
- Custom (paste your own JD)

### 📊 Analytics Dashboard (4 Tabs)
- **Tab 1 — Rankings:** Per-candidate score cards with donut charts and skill badges
- **Tab 2 — Full Report:** Complete table + CSV download

---

## 🛠️ Tech Stack

| Category | Tools Used |
|---|---|
| Language | Python 3.10+ |
| Web UI | Streamlit |
| NLP | spaCy, NLTK |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Similarity | Cosine Similarity (scikit-learn) |
| File Parsing | pdfplumber, python-docx |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |

---

## 📁 Project Structure

```
AI_Resume_Screening_System/
│
├── app.py                      # Main Streamlit web application
│
├── src/
│   ├── __init__.py             # Package init
│   ├── parser.py               # PDF/DOCX text extraction
│   ├── preprocess.py           # NLP text cleaning (lowercase, lemmatize, stopwords)
│   ├── matcher.py              # Sentence Transformer embeddings + cosine similarity
│   ├── skill_extractor.py      # Skill detection and gap analysis
│   └── ranker.py               # Candidate ranking engine
│
├── data/
│   ├── resumes/                # Upload sample resumes here
│   └── job_descriptions/       # Sample job descriptions
│
├── models/                     # Cached embedding models
│
├── requirements.txt            # All Python dependencies
└── README.md                   # This file
```

---

## 🚀 Installation & Setup

### Step 1 — Clone the Repository
```bash
git clone https://github.com/KetanRokade/AI_Resume_Screening_System.git
cd AI_Resume_Screening_System
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 3 — Run the App
```bash
streamlit run app.py
```

### Step 4 — Open in Browser
```
http://localhost:8501
```

---

## 📦 Requirements

```
streamlit>=1.32.0
pdfplumber>=0.10.0
python-docx>=1.1.0
sentence-transformers>=2.7.0
scikit-learn>=1.4.0
pandas>=2.1.0
nltk>=3.8.1
spacy>=3.7.0
numpy>=1.26.0
plotly>=5.18.0
```

---

## 🧠 How It Works — Full Pipeline

```
Step 1: User uploads PDF/DOCX resumes + pastes Job Description
        ↓
Step 2: Document Parser (pdfplumber / python-docx)
        → Extracts plain text from each resume
        ↓
Step 3: NLP Preprocessing (NLTK + spaCy)
        → Lowercase, remove stop words, lemmatization
        → Skill normalization (ML = machine learning)
        ↓
Step 4: Sentence Transformer Embedding
        → Resume text → vector [0.23, -0.87, 0.45, ...]
        → JD text     → vector [0.21, -0.90, 0.42, ...]
        ↓
Step 5: Cosine Similarity
        → Score = cos(resume_vector, jd_vector)
        → Example: 0.87 = 87% match
        ↓
Step 6: Skill Extraction
        → Find matched skills, missing skills, bonus skills
        ↓
Step 7: Ranking Engine
        → Sort by score (descending)
        → Apply minimum threshold filter
        ↓
Step 8: Web UI Dashboard
        → Display ranked results, charts, skill heatmap, CSV export
```

---

## 📊 Example Output

| Rank | Candidate | Match Score | Matched Skills | Missing Skills |
|---|---|---|---|---|
| 🥇 1 | Vikram_Das | 94.2% | python, ml, nlp, bert, docker | — |
| 🥈 2 | Alice_Sharma | 88.7% | python, tensorflow, nlp, pandas | kubernetes |
| 🥉 3 | Sneha_Kulkarni | 85.3% | python, nlp, bert, hugging face | docker |
| #4 | Rahul_Verma | 71.4% | python, deep learning, aws | nlp, bert |
| #5 | Deepika_Rao | 58.2% | python, scikit-learn, pandas | nlp, docker |

---

## 🔍 Why Sentence Transformers over TF-IDF?

| Feature | TF-IDF | Sentence Transformers |
|---|---|---|
| Word frequency | ✅ | ✅ |
| Semantic meaning | ❌ | ✅ |
| "ML" = "machine learning" | ❌ | ✅ |
| Context understanding | ❌ | ✅ |
| Speed | ⚡ Fast | 🧠 Slightly slower but smarter |

---

## 🎤 Interview Talking Points

**Q: Why did you build this project?**
> "I wanted to solve a real-world HR problem using NLP and ML. Resume screening is time-consuming and inconsistent when done manually. This system automates it with AI."

**Q: Why Sentence Transformers instead of TF-IDF?**
> "TF-IDF fails on semantic similarity. If the JD says 'machine learning' and the resume says 'ML', TF-IDF gives 0% match. Sentence Transformers understand they mean the same thing."

**Q: How is cosine similarity calculated?**
> "Both the resume and JD are converted to embedding vectors. Cosine similarity measures the angle between them — 1.0 means identical meaning, 0.0 means completely different."

**Q: How do you extract skills?**
> "I use a master skills database of 100+ skills with regex word-boundary matching. I also normalize terms — C++ becomes cplusplus, C# becomes csharp — to avoid mismatches."

**Q: How does the ATS score work?**
> "It checks formatting signals like presence of email, phone, LinkedIn, section headers, and keyword density relative to the job description."

**Q: How do you reduce bias?**
> "The system only looks at professional content — skills, experience, and education. It ignores names, gender, and personal identifiers."

---

## 🔮 Future Improvements

- [ ] LLM-based explanation ("Why was this candidate ranked #1?")
- [ ] Bias detection and fairness audit module
- [ ] Online deployment on Streamlit Cloud / HuggingFace Spaces
- [ ] Interview question generator based on skill gaps
- [ ] Cover letter analysis
- [ ] LinkedIn profile scraping integration
- [ ] Feedback loop for HR to re-train rankings

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ by Ketan Rokade**

⭐ If you found this project helpful, please give it a star on GitHub!
