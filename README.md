# 🤖 AI Resume Screening System

An AI-powered Resume Screening System that automatically analyzes, ranks, and compares resumes against a Job Description using NLP and Machine Learning techniques.

## 🚀 Features

* Upload multiple resumes (PDF/DOCX)
* Extract resume text automatically
* Compare resumes with Job Description
* AI-powered candidate ranking
* Skill extraction and gap analysis
* ATS score evaluation
* Resume match percentage
* Interactive Streamlit dashboard
* CSV report download

## 🛠️ Tech Stack

* Python
* Streamlit
* Sentence Transformers
* Scikit-learn
* spaCy
* NLTK
* Pandas
* NumPy
* Plotly
* pdfplumber
* python-docx

## 📂 Project Structure

```text
AI_Resume_Screening_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── parser.py
│   ├── preprocess.py
│   ├── matcher.py
│   ├── skill_extractor.py
│   └── ranker.py
│
└── data/
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/KetanRokade/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Run the application:

```bash
streamlit run app.py
```

## 🧠 How It Works

1. Upload resumes.
2. Paste Job Description.
3. Extract and preprocess text.
4. Generate embeddings using Sentence Transformers.
5. Calculate cosine similarity.
6. Extract skills and identify gaps.
7. Rank candidates based on match score.
8. Display results in Streamlit dashboard.

## 📊 Example Use Cases

* HR Resume Screening
* Talent Acquisition
* Recruitment Automation
* Candidate Ranking
* Skill Gap Analysis

## 🔮 Future Enhancements

* LLM-based candidate explanations
* Interview question generation
* Resume recommendations
* Cloud deployment
* Advanced ATS scoring

## 👨‍💻 Author

**Ketan Rokade**

AI/ML Engineer | Data Analyst | NLP Enthusiast

## 📄 License

This project is licensed under the MIT License.
