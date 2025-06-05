import os
import streamlit as st
import PyPDF2
import docx
import spacy
import re
import pyperclip
import json
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Skill keywords
SKILL_KEYWORDS = [
    'python', 'java', 'javascript', 'sql', 'c++', 'c#', 'ruby', 'php',
    'html', 'css', 'node.js', 'react', 'angular', 'vue.js', 'flutter',
    'android', 'ios', 'machine learning', 'deep learning', 'ai', 'tensorflow',
    'pytorch', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
    'scrum', 'agile', 'nosql', 'mongodb', 'postgresql', 'mysql',
    'data analysis', 'data science', 'big data', 'hadoop', 'spark',
    'nlp', 'computer vision', 'data visualization'
]

BLACKLIST_TERMS = [
    "project", "experience", "title", "portfolio", "training", "internship",
    "summary", "contact", "email", "phone", "address", "linkedin", "skills"
]

# Location keywords to avoid false positives for names
LOCATION_KEYWORDS = [
    "andhra", "pradesh", "arunachal", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
    "haryana", "himachal", "jammu", "kashmir", "jharkhand", "karnataka", "kerala", "madhya",
    "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab",
    "rajasthan", "sikkim", "tamil", "nadu", "telangana", "tripura", "uttar", "uttarakhand", "west",
    "bengal", "delhi", "hyderabad", "mumbai", "chennai", "bangalore", "kolkata", "bhopal",
    "pune", "visakhapatnam", "kochi", "indore", "vijayawada"
]

# --- Text extraction helpers ---

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

# --- Extraction logic ---

def extract_name(text):
    lines = text.strip().split('\n')[:10]  # Check only top 10 lines
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue  # Skip empty lines

        # Ignore lines that clearly aren't names
        if any(word in cleaned.lower() for word in ["resume", "curriculum vitae", "cv", "profile", "andhra", "orissa", "contact", "email", "phone", "address"]):
            continue

        # Very basic filter: skip lines with too many words (not a name)
        if len(cleaned.split()) > 4:
            continue

        return cleaned  # Return the first good candidate

    return "Not found"


def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s().-]{7,}\d', text)
    return match.group() if match else "Not found"

def extract_skills(text):
    text = text.lower()
    for term in BLACKLIST_TERMS:
        text = re.sub(rf'\b{term}\b', '', text)
    found_skills = {skill for skill in SKILL_KEYWORDS if skill in text}
    return sorted(found_skills)

def extract_experience(text):
    lines = text.split('\n')
    experience = []
    capture = False
    for line in lines:
        if "experience" in line.lower():
            capture = True
            continue
        if capture:
            if line.strip() == "":
                break
            experience.append(line)
    return "\n".join(experience).strip() if experience else "Not found"

# --- Streamlit app ---

def main():
    st.title("📄 Resume Skill Extractor")

    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
    if uploaded_file:
        with open("temp_resume", "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf("temp_resume")
            else:
                text = extract_text_from_docx("temp_resume")

            name = extract_name(text)
            email = extract_email(text)
            phone = extract_phone(text)
            skills = extract_skills(text)
            experience = extract_experience(text)

            st.header("🔍 Extracted Resume Data")
            st.subheader("👤 Name")
            st.write(name)

            st.subheader("📧 Email")
            st.write(email)

            st.subheader("📞 Phone")
            st.write(phone)

            st.subheader("💡 Skills")
            if skills:
                skill_text = "\n".join(skills)
                st.text_area("Skill List", skill_text, height=200)
                if st.button("📋 Copy Skills to Clipboard"):
                    pyperclip.copy(skill_text)
                    st.success("Skills copied to clipboard!")
                st.download_button(
                    label="📥 Download Skills",
                    data=skill_text,
                    file_name="extracted_skills.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No recognizable skills found.")

            st.subheader("💼 Work Experience")
            st.text_area("Experience", experience, height=150)

            result = {
                "name": name,
                "email": email,
                "phone": phone,
                "skills": skills,
                "experience": experience
            }

            st.download_button(
                label="📥 Download Full Data (.json)",
                data=json.dumps(result, indent=4),
                file_name="resume_data.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error processing resume: {e}")
        finally:
            os.remove("temp_resume")

if __name__ == "__main__":
    main()

