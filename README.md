# Resume Skill Extractor 🧠

A simple, Dockerized, GUI-based Streamlit application that extracts **skills** from PDF and DOCX resumes using NLP and keyword matching.

---

## 🔍 Features

- Upload resume files (PDF/DOCX)
- Extract skills using NLP (spaCy + regex matching)
- Display a clean list of skills
- Copy skills to clipboard ✅
- Download extracted skills as a `.txt` file
- Dockerized for easy deployment

---

## 🚀 How to Run

### 🧪 Run Locally (Python)

```bash
pip install -r requirements.txt
streamlit run app.py

### 3. 🐳 Run by Cloning Repo

```bash
git clone https://github.com/DhanyaDeepika/resume-skill-extractor.git
cd resume-skill-extractor
pip install -r requirements.txt
streamlit run app.py

